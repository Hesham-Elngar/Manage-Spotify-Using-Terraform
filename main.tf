terraform {
  required_providers {
    spotify = {
      source = "louishuyng/spotify"
      version = "0.3.6"
    }
  }
}

provider "spotify" {
  api_key = var.api_key
}


resource "spotify_playlist" "playlist" {
  name        = "My playlist by terraform"
  description = "My Musical Taste is so awesome"
  public      = false

  tracks = [
    data.spotify_track.Aloomek.id,
    data.spotify_track.Hesseny.id,
    data.spotify_track.WALAMEEN.id,
  ]
}

data "spotify_track" "Aloomek" {
  url = "https://open.spotify.com/track/4U7uW9KlqalDKu8ff9OyDm"
}
data "spotify_track" "Hesseny" {
  url = "https://open.spotify.com/track/4U7uW9KlqalDKu8ff9OyDm"
}
data "spotify_track" "WALAMEEN" {
  url = "https://open.spotify.com/track/52Jft3EkjHz3YizhXvuftP"
}
