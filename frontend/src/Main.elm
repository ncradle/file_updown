module Main exposing (..)

import Browser
import File exposing (File)
import File.Download as Download
import File.Select as Select
import Html exposing (Html, button, div, h1, text)
import Html.Events exposing (onClick)
import Http exposing (Error(..))



-- MAIN


main : Program () Model Msg
main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }



-- MODEL


type alias Model =
    { text : String
    , file : Downloader
    }


init : () -> ( Model, Cmd Msg )
init _ =
    ( Model "" NotYet, Cmd.none )



-- UPDATE


type Msg
    = CsvRequested
    | CsvSelected File
    | Uploaded (Result Http.Error String)


type Downloader
    = NotYet
    | Ready


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        CsvRequested ->
            ( Model "" NotYet
            , Select.file [] CsvSelected
            )

        CsvSelected file ->
            ( model
            , Http.post
                { url = "http://localhost:5000/upload"
                , body = Http.multipartBody [ Http.filePart "uploaded" file ]
                , expect = Http.expectString Uploaded
                }
            )

        Uploaded result ->
            case result of
                Ok text ->
                    ( Model text Ready, Download.string "result.txt" "text/plain" text )

                Err err ->
                    case err of
                        BadUrl badurl ->
                            ( { model | text = "Bad url :" ++ badurl }, Cmd.none )

                        Timeout ->
                            ( { model | text = "Timeout" }, Cmd.none )

                        NetworkError ->
                            ( { model | text = "Network error" }, Cmd.none )

                        BadStatus status ->
                            ( { model | text = "Bad status : " ++ String.fromInt status }, Cmd.none )

                        BadBody badBody ->
                            ( { model | text = "Bad body : " ++ badBody }, Cmd.none )



-- VIEW


view : Model -> Html Msg
view model =
    div []
        [ button [ onClick CsvRequested ] [ text "Load txt" ]
        , h1 [] [ text model.text ]
        ]



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none
