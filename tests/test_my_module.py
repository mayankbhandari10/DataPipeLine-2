import unittest
from unittest.mock import Mock, patch
from WeatherDataProducer import get_and_save_weather_data


class TestGetAndSaveWeatherData(unittest.TestCase):
    @patch("WeatherDataProducer.requests.get")
    @patch("WeatherDataProducer.Producer")
    def test_get_and_save_weather_data(self, mock_Producer, mock_requests_get):
        # Mock the response from requests.get
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"temperature": 25.0}
        mock_requests_get.return_value = mock_response

        # Mock the Kafka producer
        mock_producer_instance = mock_Producer.return_value
        mock_producer_instance.produce.return_value = None

        # Call the function
        get_and_save_weather_data()

        # Assertions
        mock_requests_get.assert_called_once()
        mock_producer_instance.produce.assert_called_once()
        mock_producer_instance.flush.assert_called_once()

    @patch("WeatherDataProducer.requests.get")
    @patch("WeatherDataProducer.Producer")
    def test_get_and_save_weather_data_request_failure(
        self, mock_Producer, mock_requests_get
    ):
        # Mock the response from requests.get
        mock_response = Mock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Mock the Kafka producer
        mock_producer_instance = mock_Producer.return_value
        mock_producer_instance.produce.return_value = None

        # Call the function
        get_and_save_weather_data()

        # Assertions
        mock_requests_get.assert_called_once()
        mock_producer_instance.produce.assert_not_called()

    @patch("WeatherDataProducer.requests.get")
    @patch("WeatherDataProducer.Producer")
    def test_get_and_save_weather_data_kafka_failure(
        self, mock_Producer, mock_requests_get
    ):
        # Mock the response from requests.get
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"temperature": 25.0}
        mock_requests_get.return_value = mock_response

        # Mock the Kafka producer
        mock_producer_instance = mock_Producer.return_value
        mock_producer_instance.produce.return_value = None
        mock_producer_instance.flush.return_value = None

        # Call the function
        get_and_save_weather_data()

        # Assertions
        mock_requests_get.assert_called_once()
        mock_producer_instance.produce.assert_called_once()
        mock_producer_instance.flush.assert_called_once()


if __name__ == "__main__":
    unittest.main()
