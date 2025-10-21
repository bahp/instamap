import instaloader
import sys

YOUR_USERNAME = "bahp.dev"

try:
    L = instaloader.Instaloader(
        download_geotags=True,
        save_metadata=True,
        download_pictures=False,  # Set to False if you only want metadata
        download_videos=False,
        compress_json=False,
        download_video_thumbnails=False
    )

    # --- Secure Login (Required) ---
    try:
        print(f"Loading session for {YOUR_USERNAME}...")
        L.load_session_from_file(YOUR_USERNAME)
        print("Session loaded.")
    except FileNotFoundError:
        L.interactive_login(YOUR_USERNAME)

    # --- Get the Post Generator ---
    print("Checking for new saved posts...")
    saved_posts_generator = L.download_saved_posts(
        fast_update=True, target=YOUR_USERNAME
    )

    saved_posts_generator = L.get_saved_posts()
    for post in saved_posts_generator:
        # Here, 'target' tells download_post to save inside the ':saved' folder
        was_downloaded = L.download_post(post)
        if not was_downloaded:
            break  # Stop if already downloaded

    """
    new_posts_found = 0

    # Loop through the generator (newest posts first)
    for post in saved_posts_generator[:5]:
        # L.download_post() returns True if it downloads,
        # and False if it skips (already exists)
        was_downloaded = L.download_post(post, target=":saved")

        if was_downloaded:
            print(f"Downloaded new post: {post.shortcode}")
            new_posts_found += 1
        else:
            # This post was already downloaded.
            # Since posts are in order, we can stop the loop.
            print(f"Found already-downloaded post ({post.shortcode}). Stopping.")
            break

    if new_posts_found == 0:
        print("No new saved posts found.")
    else:
        print(f"Successfully downloaded {new_posts_found} new posts.")

    print("Saved posts update complete.")
    """

except instaloader.exceptions.ConnectionException as e:
    print(f"Error: {e}", file=sys.stderr)
except FileNotFoundError:
    print(f"Error: Session file not found for '{YOUR_USERNAME}'.", file=sys.stderr)
except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)