from __future__ import unicode_literals

from django.test import override_settings

from rest_framework import status

from documents.tests import DocumentTestMixin
from rest_api.tests import BaseAPITestCase

from ..permissions import (
    permission_ocr_document, permission_ocr_content_view,
)

TEST_DOCUMENT_CONTENT = 'Mayan EDMS Documentation'


@override_settings(OCR_AUTO_OCR=False)
@override_settings(DOCUMENT_PARSING_PDFTOTEXT_PATH='')
class OCRAPITestCase(DocumentTestMixin, BaseAPITestCase):
    """
    Test the OCR app API endpoints
    """
    def setUp(self):
        super(OCRAPITestCase, self).setUp()
        self.login_user()

    def _request_document_ocr_submit_view(self):
        return self.post(
            viewname='rest_api:document-ocr-submit-view',
            args=(self.document.pk,)
        )

    def test_submit_document_no_access(self):
        response = self._request_document_ocr_submit_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertFalse(hasattr(self.document.pages.first(), 'ocr_content'))

    def test_submit_document_with_access(self):
        self.grant_access(
            permission=permission_ocr_document, obj=self.document
        )
        response = self._request_document_ocr_submit_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertTrue(hasattr(self.document.pages.first(), 'ocr_content'))

    def _request_document_version_ocr_submit_view(self):
        return self.post(
            viewname='rest_api:document-version-ocr-submit-view',
            args=(self.document.pk, self.document.latest_version.pk,)
        )

    def test_submit_document_version_no_access(self):
        response = self._request_document_version_ocr_submit_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertFalse(hasattr(self.document.pages.first(), 'ocr_content'))

    def test_submit_document_version_with_access(self):
        self.grant_access(
            permission=permission_ocr_document, obj=self.document
        )
        response = self._request_document_version_ocr_submit_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertTrue(hasattr(self.document.pages.first(), 'ocr_content'))

    def _request_document_page_content_view(self):
        return self.get(
            viewname='rest_api:document-page-ocr-content-view',
            args=(
                self.document.pk, self.document.latest_version.pk,
                self.document.latest_version.pages.first().pk,
            )
        )

    def test_get_document_version_page_content_no_access(self):
        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_document_version_page_content_with_access(self):
        self.document.submit_for_ocr()
        self.grant_access(
            permission=permission_ocr_content_view, obj=self.document
        )
        response = self._request_document_page_content_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            TEST_DOCUMENT_CONTENT in response.data['content']
        )
