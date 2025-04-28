# Photo Album Application

A cloud-based photo album application that enables users to upload images and search through them using natural language queries. The application leverages AWS services including Rekognition for image analysis, Lex for natural language processing, and OpenSearch for efficient image retrieval.

Team Members: Abhishek Adinarayanappa (aa12037), Adithya Balachandra (ab12095)

## Architecture Overview

The application follows a serverless architecture pattern using the following AWS services:

- **S3**: Stores the frontend assets and image files
- **Lambda**: Handles image indexing and search functionality
- **API Gateway**: Provides REST API endpoints
- **Amazon Lex**: Processes natural language search queries
- **Amazon Rekognition**: Detects objects and scenes in images
- **OpenSearch Service**: Indexes and searches image metadata
- **CloudFormation**: Defines infrastructure as code
- **CodePipeline**: Automates deployment workflows

## Features

- **Image Upload**: Upload photos with custom labels
- **Image Analysis**: Automatic object and scene detection using Amazon Rekognition
- **Natural Language Search**: Search photos using conversational language
- **Responsive UI**: Modern, responsive interface for browsing and searching photos

## Project Structure

```
CC-Assignment3-Photo-Album/
├── Frontend/
│   ├── README.md
│   ├── apiGateway-js-sdk/    # Generated SDK from API Gateway
│   ├── index.html            # Main frontend page
│   ├── index.js              # Frontend JavaScript logic
│   ├── search images.jpeg    # Sample image
│   └── style.css             # Frontend styling
├── LambdaFunctions/
│   ├── index-photos.py       # Lambda function for indexing photos
│   └── search-photos.py      # Lambda function for searching photos
├── README.md                 # Main project README
├── images/                   # Sample images for testing
│   ├── cat.jpeg
│   ├── dogs.jpeg
│   ├── dogs1.jpeg
│   ├── sample_image.jpg
│   └── scenery.jpg
└── other/
    ├── CloudFormation/
    │   └── template.yaml     # CloudFormation template
    └── CodePipeline/
        ├── Backend/
        │   └── buildspec.yaml # Backend deployment specification
        └── Frontend/
            └── buildspec.yaml # Frontend deployment specification
```

## API Reference

The application exposes the following API endpoints:

### PUT /upload/{bucket}/{filename}

Uploads an image to the S3 bucket.

**Path Parameters**:

- bucket: The S3 bucket name (e.g., "my-b2-photos")
- filename: The name of the file to be uploaded

**Headers**:

- Content-Type: image/jpeg (or other image types)
- x-amz-meta-customLabels: Comma-separated list of custom labels

### GET /search

Searches for photos based on query text.

**Parameters**:

- q: Search query (e.g., "Show me pictures of dogs")

**Response**:

```json
[
  {
    "objectKey": "my-photo.jpg",
    "bucket": "my-photo-bucket",
    "createdTimestamp": "2018-11-05T12:40:02",
    "labels": ["person", "dog", "ball", "park"]
  }
]
```

## Components Overview

### Frontend

The frontend is a responsive web application with:

- Search interface for natural language queries
- Image gallery to display search results
- Upload functionality with custom label support

### Lambda Functions

#### index-photos (LF1)

This function is triggered when a new photo is uploaded to S3:

- Extracts labels using Amazon Rekognition
- Retrieves custom labels from S3 object metadata
- Indexes the photo metadata in OpenSearch

#### search-photos (LF2)

This function handles search queries:

- Uses Amazon Lex to extract keywords from natural language queries
- Searches OpenSearch for photos matching the keywords
- Returns matching photos to the frontend

### Development

#### Frontend Development

The frontend is a simple HTML/CSS/JavaScript application that uses the API Gateway SDK to communicate with the backend services.

To modify the frontend:

1. Edit the HTML, CSS, and JavaScript files in the `Frontend` directory
2. Deploy using the CodePipeline or manually upload to the S3 bucket

#### Backend Development

The backend consists of two Lambda functions in the `LambdaFunctions` directory:

- **index-photos.py**: Processes newly uploaded images, extracts labels using Rekognition, and indexes metadata in OpenSearch
- **search-photos.py**: Processes search queries using Lex and retrieves matching photos from OpenSearch

## Infrastructure as Code

## CI/CD Pipeline

Continuous Integration and Deployment is implemented using AWS CodePipeline:

- **Frontend Pipeline**: Automatically deploys frontend code changes to the S3 website bucket
  - Configuration in `other/CodePipeline/Frontend/buildspec.yaml`

- **Backend Pipeline**: Builds and deploys Lambda functions
  - Configuration in `other/CodePipeline/Backend/buildspec.yaml`
