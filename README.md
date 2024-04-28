# DiscordBot-GeminiAI
  <a href="https://www.python.org/downloads/">
    <img alt="PyPI - Python Version" src="https://img.shields.io/badge/pyversion-3.10%2B-blue?style=flat&label=python">
  </a>

[![Try with Replit Badge](https://replit.com/badge?caption=Try%20with%20Replit)](https://replit.com/@dd8611706/DiscordBot-GeminiAI?v=1#README.md)

### Gemini Demo
![demo1](https://i.imgur.com/OO52TfC.gif)

### Bard (Gemini web) Demo
![demo2](https://i.imgur.com/1U5kBJ0.png)

## Update
> ### 2024/4/28：Support [Bard](https://gemini.google.com).
> ### 2023/2/16：Add Gemini 1.0 Pro model.
   
## Features
<details>
   <summary>
   
   ### Slash command

   </summary>
   
* `/api_key setting-gemini [choice] [api_key]`
  * Can upload own google api key or delete it. (api key get from https://makersuite.google.com/app/apikey)
    * [choice]：`delete` or `set` your api key.
  
* `/gemini conversation [model] [type] [use_prompt] [use_character]`
  * Create a thread exclusively for the user to chat with the bot.
    * [model]：Choose AI model.
    * [type]：Choose thread type, private or public.
    * [temperature]：Controls the level of randomness in the output, ranging from highly varied (closer to 1.0) to less surprising (closer to 0.0).
    * [harrassment], [hate_speech], [sexually_explicit], [dangerous_content]：It's [Safety Settings](https://ai.google.dev/docs/safety_setting_gemini#safety-settings), the default is `Block some`.

* `/cookies setting-bard [choice] [secure_1psid] [secure_1psidts]`
  * Can upload own Bard Cookies or delete it.
    * [choice]：`delete` or `set` your Bard Cookies.
    * [secure_1psid], [secure_1psidts]：Required Cookie Parameters.

* `/Bard conversation [type]`
  * Create a Bard thread exclusively for the user to chat with the bot.
    * [type]：Choose thread type, private or public.

</details>

## Usage

### Install

```
pip install -r requirements.txt
```

### Discord bot permission

![permission](https://i.imgur.com/ZHYlRJH.png)

### Get Bard Cookies

> [!IMPORTANT]  
> Since too many people using the same cookies may cause errors, it is recommended to ask the person who wants to use it to upload his/her own cookies.

* Go to https://gemini.google.com and login with your Google account
* Press F12 for web inspector, go to `Network` tab and refresh the page
* Click any request and copy cookie values of `__Secure-1PSID` and `__Secure-1PSIDTS`

### .env setting
Rename the file`.env.dev`to`.env`, then open it and edit it.
```markdown
DISCORD_BOT_TOKEN=

# Can get from https://makersuite.google.com/app/apikey
GEMINI_API_KEY=

# Setting default Bard cookies
BARD_SECURE_1PSID=
BARD_SECURE_1PSIDTS=

# Allow each commands only use in some channel, if you don't set it, just default to all channels.
# specific channel(s) for `/api_key setting-gemini`
GEMINI_SETTING_CHANNEL_ID=1227670969702754857,1227327094070254857

# specific channel(s) for `/gemini conversation`
GEMINI_CHAT_CHANNEL_ID=1227327094070254857

# specific channel(s) for `/bard conversation`
BARD_CHAT_CHANNEL_ID=

# specific channel(s) for `/cookies setting-bard`
BARD_COOKIES_SETTING_CHANNEL_ID=

# specific channel(s) for `/help`
HELP_CMD_CHANNEL_ID=
```

### Start run your bot.
   ```python
   python3 bot.py

   ```

## Credits
* generative-ai-python - https://github.com/google/generative-ai-python
* Gemini-API - https://github.com/HanaokaYuzu/Gemini-API

## Contributors

This project exists thanks to all the people who contribute.

[![](https://contrib.rocks/image?repo=FuseFairy/DiscordBot-GeminiAI)](https://github.com/FuseFairy/DiscordBot-GeminiAI/graphs/contributors)