from telegram import Update
from telegram.ext import ContextTypes
import logging
import os
from typing import List


async def post_to_mastodon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle Telegram messages and post them to Mastodon.
    This function extracts text and images from the Telegram update and posts them to Mastodon.
    """
    # Initialize Mastodon client
    mastodon = context.bot_data["mastodon_object"]

    # Extract text from the message
    text = update.message.text or update.message.caption or ""

    # Extract images from the message
    photos: List[str] = []
    if update.message.photo:
        for photo in update.message.photo:
            file = await context.bot.get_file(photo.file_id)

            # Download the photo
            photo_path = f"temp_{photo.file_id}.jpg"
            await file.download_to_drive(photo_path)
            photos.append(photo_path)


    try:
        if photos:
            # Post with media
            response = mastodon.post_with_media(text, photos)
        else:
            # Post text only
            response = mastodon.post(text)

        logging.info(f"Successfully posted to Mastodon: {response}")
        await update.message.reply_text("Successfully posted to Mastodon!")

    except Exception as e:
        logging.error(f"Error posting to Mastodon: {str(e)}")
        await update.message.reply_text(
            "Failed to post to Mastodon. Please try again later."
        )
    finally:
        # Clean up downloaded photos
        for photo in photos:
            if os.path.exists(photo):
                os.remove(photo)
