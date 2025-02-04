# Weather-API

This is a Weather API built with Flask, Redis, and Visual Crossing Weather API. The API allows you to get the current weather information for a specific city. The weather data is cached using Redis to reduce the number of API calls and improve response times.

## Features

- **Weather Data Fetching**: Fetch the current weather data for a specified city.
- **Caching with Redis**: Caches weather data for 12 hours to avoid making repeated requests to the weather API.
- **Rate Limiting**: Implements rate limiting to control the number of requests that can be made per minute.

## Endpoints

### `GET /weather/<city>`

Fetches the weather data for the specified city. If the data is cached, it will return the cached result. Otherwise, it will fetch fresh data from the Visual Crossing Weather API.

#### Parameters

- `city` (string): The name of the city for which the weather data is requested.

#### Example Request

```bash
GET /weather/London
