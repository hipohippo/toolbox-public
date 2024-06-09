import re

from lxml.html.clean import Cleaner

allowed_tags = ('a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption', 'figure', 'h3', 'h4', 'hr', 'i',
                'iframe', 'img', 'li', 'ol', 'p', 'pre', 's', 'strong', 'u', 'ul', 'video')
allowed_top_level_tags = ('aside', 'blockquote', 'pre', 'figure', 'h3', 'h4', 'hr', 'ol', 'p', 'ul')

elements_with_text = ('a', 'aside', 'b', 'blockquote', 'em', 'h3', 'h4', 'p', 'strong')

youtube_re = re.compile(r'(https?:)?//(www\.)?youtube(-nocookie)?\.com/embed/')
vimeo_re = re.compile(r'(https?:)?//player\.vimeo\.com/video/(\d+)')
twitter_re = re.compile(r'(https?:)?//(www\.)?twitter\.com/[A-Za-z0-9_]{1,15}/status/\d+')
telegram_embed_iframe_re = re.compile(r'^(https?)://(t\.me|telegram\.me|telegram\.dog)/([a-zA-Z0-9_]+)/(\d+)', re.IGNORECASE)
telegram_embed_script_re = re.compile(r'''<script(?=[^>]+\sdata-telegram-post=['"]([^'"]+))[^<]+</script>''', re.IGNORECASE)
pre_content_re = re.compile(r'<(pre|code)(>|\s[^>]*>)[\s\S]*?</\1>')
line_breaks_inside_pre = re.compile(r'<br(/?>|\s[^<>]*>)')
line_breaks_and_empty_strings = re.compile(r'(\s{2,}|\s*\r?\n\s*)')
header_re = re.compile(r'<head[^a-z][\s\S]*</head>')

def clean_article_html(html_string):
    
    html_string = html_string.replace('<h1', '<h3').replace('</h1>', '</h3>')
    # telegram will convert <b> anyway
    html_string = re.sub(r'<(/?)b(?=\s|>)', r'<\1strong', html_string)
    html_string = re.sub(r'<(/?)(h2|h5|h6)', r'<\1h4', html_string)
    # convert telegram embed posts before cleaner
    html_string = re.sub(telegram_embed_script_re, r'<iframe src="https://t.me/\1"></iframe>', html_string)
    # remove <head> if present (can't do this with Cleaner)
    html_string = header_re.sub('', html_string)
    
    c = Cleaner(
        allow_tags=allowed_tags,
        style=True,
        remove_unknown_tags=False,
        embedded=False,
        safe_attrs_only=True,
        safe_attrs=('src', 'href', 'class')
    )
    # wrap with div to be sure it is there
    # (otherwise lxml will add parent element in some cases
    html_string = '<div>%s</div>' % html_string
    cleaned = c.clean_html(html_string)
    # remove wrapped div
    cleaned = cleaned[5:-6]
    # remove all line breaks and empty strings
    html_string = replace_line_breaks_except_pre(cleaned)
    # but replace multiple br tags with one line break, telegraph will convert it to <br class="inline">
    html_string = re.sub(r'(<br(/?>|\s[^<>]*>)\s*)+', '\n', html_string)
    
    return html_string.strip(' \t')

def replace_line_breaks_except_pre(html_string, replace_by=' '):
    # Remove all line breaks and empty strings, except pre tag
    # how to make it in one string? :\
    pre_ranges = [0]
    out = ''
    
    # replace non-breaking space with usual space
    html_string = html_string.replace('\u00A0', ' ')
    
    # get <pre> start/end postion
    for x in pre_content_re.finditer(html_string):
        start, end = x.start(), x.end()
        pre_ranges.extend((start, end))
    pre_ranges.append(len(html_string))
    
    # all odd elements are <pre>, leave them untouched
    for k in range(1, len(pre_ranges)):
        part = html_string[pre_ranges[k-1]:pre_ranges[k]]
        if k % 2 == 0:
            out += line_breaks_inside_pre.sub('\n', part)
        else:
            out += line_breaks_and_empty_strings.sub(replace_by, part)
    return out

def google_parse(config: dict, keyword: str) -> str:
    driver: WebDriver = config["webdriver"]
    driver.switch_to.window(driver.window_handles[1])
    driver.get(f"https://google.com/search?q={keyword}")
    driver.implicitly_wait(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    for data in soup(["style", "script"]):
        # Remove tags
        data.decompose()

    for tag in soup.find_all("span"):
        tag.unwrap()

    results = soup.find_all(class_="g")
    return "\n".join([f"{result.text}" for result in results[:3]])



async def google_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, keyword: str):
    try:
        logging.info(f"received request to google {keyword}")
        result = google_parse(context.bot_data, keyword)
        logging.info(result[:300])
        await update.message.reply_html(result)
    except Exception as error:
        logging.error(error)
        await context.bot.send_message(context.bot_data["debug_log_group"], text=error)