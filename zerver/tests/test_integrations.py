# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from django.conf import settings
from django.test import TestCase, override_settings
from six import text_type
from typing import Any

from zproject.settings import DEPLOY_ROOT
from zerver.lib.integrations import INTEGRATIONS
from zerver.views.integrations import add_api_uri_context

class RequestMock(object):
    def __init__(self, host=settings.EXTERNAL_HOST):
        # type: (text_type) -> None
        self.host = host

    def get_host(self):
        # type: () -> text_type
        return self.host

class IntegrationTest(TestCase):
    def test_check_if_every_integration_has_logo_that_exists(self):
        # type: () -> None
        for integration in INTEGRATIONS.values():
            self.assertTrue(os.path.isfile(os.path.join(DEPLOY_ROOT, integration.logo)))

    @override_settings(REALMS_HAVE_SUBDOMAINS=False)
    def test_api_url_view_base(self):
        # type: () -> None
        context = dict()  # type: Dict[str, Any]
        add_api_uri_context(context, RequestMock())
        self.assertEqual(context["external_api_path_subdomain"], "zulipdev.com:9991/api")
        self.assertEqual(context["external_api_uri_subdomain"], "http://zulipdev.com:9991/api")

    @override_settings(REALMS_HAVE_SUBDOMAINS=True)
    def test_api_url_view_subdomains_base(self):
        # type: () -> None
        context = dict()  # type: Dict[str, Any]
        add_api_uri_context(context, RequestMock())
        self.assertEqual(context["external_api_path_subdomain"], "yourZulipDomain.zulipdev.com:9991/api")
        self.assertEqual(context["external_api_uri_subdomain"], "http://yourZulipDomain.zulipdev.com:9991/api")

    @override_settings(REALMS_HAVE_SUBDOMAINS=True, EXTERNAL_HOST="zulipdev.com")
    def test_api_url_view_subdomains_full(self):
        # type: () -> None
        context = dict()  # type: Dict[str, Any]
        request = RequestMock(host="mysubdomain.zulipdev.com")
        add_api_uri_context(context, request)
        self.assertEqual(context["external_api_path_subdomain"], "mysubdomain.zulipdev.com:9991/api")
        self.assertEqual(context["external_api_uri_subdomain"], "http://mysubdomain.zulipdev.com:9991/api")
