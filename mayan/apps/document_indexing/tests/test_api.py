from __future__ import unicode_literals

from rest_framework import status

from documents.tests import DocumentTestMixin
from rest_api.tests import BaseAPITestCase

from ..models import Index
from ..permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_view
)

from .literals import TEST_INDEX_LABEL, TEST_INDEX_SLUG
from .mixins import DocumentIndexingTestMixin


class DocumentIndexingAPITestCase(DocumentIndexingTestMixin, DocumentTestMixin, BaseAPITestCase):
    auto_upload_document = False

    def setUp(self):
        super(DocumentIndexingAPITestCase, self).setUp()
        self.login_user()

    def _request_index_create_api_view(self):
        return self.post(
            viewname='rest_api:index-list', data={
                'label': TEST_INDEX_LABEL, 'slug': TEST_INDEX_SLUG,
                'document_types': self.document_type.pk
            }
        )

    def test_index_create_api_view_no_permission(self):
        response = self._request_index_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Index.objects.count(), 0)

    def test_index_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_document_indexing_create)

        response = self._request_index_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        index = Index.objects.first()

        self.assertEqual(response.data['id'], index.pk)
        self.assertEqual(response.data['label'], index.label)

        self.assertEqual(Index.objects.count(), 1)
        self.assertEqual(index.label, TEST_INDEX_LABEL)

    def _request_index_delete_api_view(self):
        return self.delete(
            viewname='rest_api:index-detail', kwargs={
                'pk': self.index.pk
            }
        )

    def test_index_delete_api_view_no_permission(self):
        self._create_index()

        response = self._request_index_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(self.index in Index.objects.all())

    def test_index_delete_api_view_with_access(self):
        self._create_index()

        self.grant_access(
            obj=self.index, permission=permission_document_indexing_delete
        )

        response = self._request_index_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertTrue(self.index not in Index.objects.all())

    def _request_index_detail_api_view(self):
        return self.get(
            viewname='rest_api:index-detail', kwargs={
                'pk': self.index.pk
            }
        )

    def test_index_detail_api_view_no_access(self):
        self._create_index()

        response = self._request_index_detail_api_view()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue('id' not in response.data)

    def test_index_detail_api_view_with_access(self):
        self._create_index()

        self.grant_access(
            obj=self.index, permission=permission_document_indexing_view
        )

        response = self._request_index_detail_api_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.index.pk
        )
