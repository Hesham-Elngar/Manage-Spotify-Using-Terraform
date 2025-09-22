output "authentication_status" {
  value = data.http.spotify_me.status_code == 200 ? "✅ Successful" : "❌ Failed"
}

output "user_display_name" {
  value = try(jsondecode(data.http.spotify_me.response_body).display_name, "Unknown")
}

output "track_details" {
  value = {
    for track, req in data.http.tracks : track => {
      name    = try(jsondecode(req.response_body).name, "Not found")
      artists = try([for artist in jsondecode(req.response_body).artists : artist.name], [])
    }
  }
}

output "playlist_creation_status" {
  value = data.http.create_playlist.status_code == 201 ? "✅ Created" : "❌ Failed"
}

output "tracks_addition_status" {
  value = data.http.add_tracks.status_code == 201 ? "✅ Added" : "❌ Failed"
}

output "playlist_info" {
  value = try(
    {
      name = jsondecode(data.http.create_playlist.response_body).name
      id   = jsondecode(data.http.create_playlist.response_body).id
      url  = jsondecode(data.http.create_playlist.response_body).external_urls.spotify
    },
    {
      error = "Playlist details unavailable"
    }
  )
}

output "operation_summary" {
  value = <<EOT
Spotify Terraform Project Results:
──────────────────────────────────
Authentication: ${data.http.spotify_me.status_code == 200 ? "✅ Success" : "❌ Failed"}
Playlist Creation: ${data.http.create_playlist.status_code == 201 ? "✅ Success" : "❌ Failed"}  
Tracks Addition: ${data.http.add_tracks.status_code == 201 ? "✅ Success" : "❌ Failed"}

User: ${try(jsondecode(data.http.spotify_me.response_body).display_name, "Unknown")}
Playlist: ${try(jsondecode(data.http.create_playlist.response_body).name, "Not created")}
EOT
}
