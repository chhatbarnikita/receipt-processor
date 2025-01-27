# Receipt processor

An app that accepts a receipt, processes to it to count points and returns the points.

## Technologies used

- Python v3.9
- Flask
- Postman (API testing)

## Docker

Included the docker file that can be used to run the application. Assuming that docker is installed and running, steps to run the application:

#### Create docker image for the app

```
docker build --tag receipt-processor-docker .
```

#### Run the docker image

```
docker run -p 8080:5000 receipt-processor-docker
```

Docker will run on port `8080` while the flask app inside the container is running on port `5000`. If you have any application running on port `8080`, run docker with another free port. Make sure to use that port when calling the APIs.

## Test API endpoints

I used POSTMAN to test these endpoints.

### Process points
`POST http://127.0.0.1:8080/receipts/process` - add receipt into the body

Returns a receipt ID
```
{
    "id": "cbca3b11-1ff5-44c0-98aa-e7d6e4a882df"
}
```
``` NOTE: 400 error is thrown for invalid receipt ```

### Get total points
`GET http://127.0.0.1:8080/receipts/<receipt_id>/points` - add the receipt id from above api

Return total points if the ID is valid else return null.
```
{
    "points": 109
}
```
