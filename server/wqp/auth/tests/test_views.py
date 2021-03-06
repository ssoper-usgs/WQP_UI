
from unittest import TestCase, mock

from flask import session

from ... import app
from ..views import authentication_required_when_configured


class TestAuthenticationRequiredWhenConfigured(TestCase):
    mock_time = mock.Mock()
    mock_time.return_value = 1234567

    def setUp(self):
        self.app_client = app.test_client()

    def test_no_authentication(self):
        view_mock = mock.Mock()
        app.config['WATERAUTH_AUTHORIZE_URL'] = ''
        with app.test_request_context('/mock'):
            authentication_required_when_configured(view_mock)()

        view_mock.assert_called()

    def test_authentication_no_expiration_time(self):
        view_mock = mock.Mock()
        app.config['WATERAUTH_AUTHORIZE_URL'] = 'https://fake.auth.com'
        with app.test_request_context('/mock'):
            authentication_required_when_configured(view_mock)()

        view_mock.assert_not_called()

    @mock.patch('time.time', mock_time)
    def test_authentication_expiration_time_earlier_than_current_time(self):
        view_mock = mock.Mock()
        app.config['WATERAUTH_AUTHORIZE_URL'] = 'https://fake.auth.com'
        with app.test_request_context('/mock'):
            session['access_token_expires_at'] = 1234566
            authentication_required_when_configured(view_mock)()

        view_mock.assert_not_called()

    @mock.patch('time.time', mock_time)
    def test_authentication_expiration_time_later_than_current_time(self):
        view_mock = mock.Mock()
        app.config['WATERAUTH_AUTHORIZE_URL'] = 'https://fake.auth.com'
        with app.test_request_context('/mock'):
            session['access_token_expires_at'] = 1234568
            authentication_required_when_configured(view_mock)()

        view_mock.assert_called()
