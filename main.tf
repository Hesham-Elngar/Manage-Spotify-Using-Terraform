terraform {
  required_providers {
    http = {
      source  = "hashicorp/http"
      version = "~> 3.0"
    }
  }
}

provider "http" {}

# Test authentication first
data "http" "spotify_me" {
  url = "https://api.spotify.com/v1/me"

  request_headers = {
    Authorization = "Bearer ${var.spotify_access_token}"
  }
}

# Example: Create playlist
data "http" "create_playlist" {
  url    = "https://api.spotify.com/v1/users/${jsondecode(data.http.spotify_me.response_body).id}/playlists"
  method = "POST"

  request_headers = {
    Authorization = "Bearer ${var.spotify_access_token}"
    Content-Type  = "application/json"
  }

  request_body = jsonencode({
    name        = "Terraform Spotify Playlist"
    description = "Playlist created with Terraform"
    public      = false
  })
}

# Example: Add tracks to playlist
data "http" "add_tracks" {
  url    = "https://api.spotify.com/v1/playlists/${jsondecode(data.http.create_playlist.response_body).id}/tracks"
  method = "POST"

  request_headers = {
    Authorization = "Bearer ${var.spotify_access_token}"
    Content-Type  = "application/json"
  }

  request_body = jsonencode({
    uris = [for id in values(var.tracks) : "spotify:track:${id}"]
  })
}

# Dynamically fetch track details
data "http" "tracks" {
  for_each = var.tracks

  url = "https://api.spotify.com/v1/tracks/${each.value}"

  request_headers = {
    Authorization = "Bearer ${var.spotify_access_token}"
  }
}
