module Comms exposing (..)

import Http
import Json.Decode
import Json.Decode.Pipeline

-- Typedefs

type alias CameraSource = 
    { sourceName: String
    , layout: String
    , maxWidth: Int
    , maxHeight: Int
    , maxFramerate: Int
    , sourceType: String
    }

type alias Camera = 
    { cameraId: String
    , sources: List CameraSource
    }

type alias CameraImage = 
    { cameraId: String
    , sourceName: String
    , imageBuffer: String
    , mimeType: String
    , width: Int
    , height: Int
    , timestampMs: Int
    , stereoMode: String
    }

type alias CameraFocus = 
    { cameraId: String
    , sourceName: String
    , imageBuffer: String
    , mimeType: String
    , width: Int
    , height: Int
    , timestampMs: Int
    , stereoMode: String
    , focusScore: Float
    }

type alias CaptureEvent = 
    { images: List ImageObject
    , orientation: GeoOrientation
    , position: Postion
    , range: Range
    , timestamp: String
    , uuid: String
    }

type alias FocusScore = 
    { focusScore: Float
    , imageUrl: String
    }

type alias GeoOrientation = 
    { geoPlatformRotation: Quaternion
    }

type alias GeoPosition = 
    { elevation: Float
    , latitude: Float
    , longitude: Float
    }

type alias ImageObject = 
    { captureEventUrl: String
    , contentUrl: String
    , focusUrl: String
    , source: String
    , thumbnailUrl: String
    }

type alias JSONLDObject = 
    { @context: String
    , @type: String
    }

type alias Postion = 
    { geoPosition: GeoPosition
    }

type alias ProblemDetails = 
    { @context: String
    , @type: String
    , detail: String
    , instance: String
    , status: Int
    , title: String
    , type: String
    }

type alias Quaternion = 
    { w: Float
    , x: Float
    , y: Float
    , z: Float
    }

type alias Range = 
    { distance: Float
    }


-- Decoders

cameraSourceDecoder : Json.Decode.Decoder CameraSource
cameraSourceDecoder = 
    Json.Decode.succeed CameraSource
            |> Json.Decode.Pipeline.required "sourceName" Json.Decode.string
                |> Json.Decode.Pipeline.required "layout" Json.Decode.string
                |> Json.Decode.Pipeline.required "maxWidth" Json.Decode.int
                |> Json.Decode.Pipeline.required "maxHeight" Json.Decode.int
                |> Json.Decode.Pipeline.required "maxFramerate" Json.Decode.int
                |> Json.Decode.Pipeline.required "sourceType" Json.Decode.string
    
cameraDecoder : Json.Decode.Decoder Camera
cameraDecoder = 
    Json.Decode.succeed Camera
            |> Json.Decode.Pipeline.required "cameraId" Json.Decode.string
                |> Json.Decode.Pipeline.required "sources" (Json.Decode.list cameraSourceDecoder)
    
cameraImageDecoder : Json.Decode.Decoder CameraImage
cameraImageDecoder = 
    Json.Decode.succeed CameraImage
            |> Json.Decode.Pipeline.required "cameraId" Json.Decode.string
                |> Json.Decode.Pipeline.required "sourceName" Json.Decode.string
                |> Json.Decode.Pipeline.required "imageBuffer" Json.Decode.string
                |> Json.Decode.Pipeline.required "mimeType" Json.Decode.string
                |> Json.Decode.Pipeline.required "width" Json.Decode.int
                |> Json.Decode.Pipeline.required "height" Json.Decode.int
                |> Json.Decode.Pipeline.required "timestampMs" Json.Decode.int
                |> Json.Decode.Pipeline.required "stereoMode" Json.Decode.string
    
cameraFocusDecoder : Json.Decode.Decoder CameraFocus
cameraFocusDecoder = 
    Json.Decode.succeed CameraFocus
            |> Json.Decode.Pipeline.required "cameraId" Json.Decode.string
                |> Json.Decode.Pipeline.required "sourceName" Json.Decode.string
                |> Json.Decode.Pipeline.required "imageBuffer" Json.Decode.string
                |> Json.Decode.Pipeline.required "mimeType" Json.Decode.string
                |> Json.Decode.Pipeline.required "width" Json.Decode.int
                |> Json.Decode.Pipeline.required "height" Json.Decode.int
                |> Json.Decode.Pipeline.required "timestampMs" Json.Decode.int
                |> Json.Decode.Pipeline.required "stereoMode" Json.Decode.string
                |> Json.Decode.Pipeline.required "focusScore" Json.Decode.float
    
captureEventDecoder : Json.Decode.Decoder CaptureEvent
captureEventDecoder = 
    Json.Decode.succeed CaptureEvent
            |> Json.Decode.Pipeline.required "images" (Json.Decode.list imageObjectDecoder)
                |> Json.Decode.Pipeline.required "orientation" geoOrientationDecoder
                |> Json.Decode.Pipeline.required "position" postionDecoder
                |> Json.Decode.Pipeline.required "range" rangeDecoder
                |> Json.Decode.Pipeline.required "timestamp" Json.Decode.string
                |> Json.Decode.Pipeline.required "uuid" Json.Decode.string
    
focusScoreDecoder : Json.Decode.Decoder FocusScore
focusScoreDecoder = 
    Json.Decode.succeed FocusScore
            |> Json.Decode.Pipeline.required "focusScore" Json.Decode.float
                |> Json.Decode.Pipeline.required "imageUrl" Json.Decode.string
    
geoOrientationDecoder : Json.Decode.Decoder GeoOrientation
geoOrientationDecoder = 
    Json.Decode.succeed GeoOrientation
            |> Json.Decode.Pipeline.required "geoPlatformRotation" quaternionDecoder
    
geoPositionDecoder : Json.Decode.Decoder GeoPosition
geoPositionDecoder = 
    Json.Decode.succeed GeoPosition
            |> Json.Decode.Pipeline.required "elevation" Json.Decode.float
                |> Json.Decode.Pipeline.required "latitude" Json.Decode.float
                |> Json.Decode.Pipeline.required "longitude" Json.Decode.float
    
imageObjectDecoder : Json.Decode.Decoder ImageObject
imageObjectDecoder = 
    Json.Decode.succeed ImageObject
            |> Json.Decode.Pipeline.required "captureEventUrl" Json.Decode.string
                |> Json.Decode.Pipeline.required "contentUrl" Json.Decode.string
                |> Json.Decode.Pipeline.required "focusUrl" Json.Decode.string
                |> Json.Decode.Pipeline.required "source" Json.Decode.string
                |> Json.Decode.Pipeline.required "thumbnailUrl" Json.Decode.string
    
jSONLDObjectDecoder : Json.Decode.Decoder JSONLDObject
jSONLDObjectDecoder = 
    Json.Decode.succeed JSONLDObject
            |> Json.Decode.Pipeline.required "@context" Json.Decode.string
                |> Json.Decode.Pipeline.required "@type" Json.Decode.string
    
postionDecoder : Json.Decode.Decoder Postion
postionDecoder = 
    Json.Decode.succeed Postion
            |> Json.Decode.Pipeline.required "geoPosition" geoPositionDecoder
    
problemDetailsDecoder : Json.Decode.Decoder ProblemDetails
problemDetailsDecoder = 
    Json.Decode.succeed ProblemDetails
            |> Json.Decode.Pipeline.required "@context" Json.Decode.string
                |> Json.Decode.Pipeline.required "@type" Json.Decode.string
                |> Json.Decode.Pipeline.required "detail" Json.Decode.string
                |> Json.Decode.Pipeline.required "instance" Json.Decode.string
                |> Json.Decode.Pipeline.required "status" Json.Decode.int
                |> Json.Decode.Pipeline.required "title" Json.Decode.string
                |> Json.Decode.Pipeline.required "type" Json.Decode.string
    
quaternionDecoder : Json.Decode.Decoder Quaternion
quaternionDecoder = 
    Json.Decode.succeed Quaternion
            |> Json.Decode.Pipeline.required "w" Json.Decode.float
                |> Json.Decode.Pipeline.required "x" Json.Decode.float
                |> Json.Decode.Pipeline.required "y" Json.Decode.float
                |> Json.Decode.Pipeline.required "z" Json.Decode.float
    
rangeDecoder : Json.Decode.Decoder Range
rangeDecoder = 
    Json.Decode.succeed Range
            |> Json.Decode.Pipeline.required "distance" Json.Decode.float
    

-- Remote calls
acquireImagesApiV1CameraGetCameraListRequest : (Result Http.Error (List Camera) -> msg) -> Cmd msg
acquireImagesApiV1CameraGetCameraListRequest toMsg =
    Http.get
      { url = "/api/v1/camera/"
      , expect = Http.expectJson toMsg (Json.Decode.list cameraDecoder) 
      }


