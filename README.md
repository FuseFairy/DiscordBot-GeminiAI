# DiscordBot-GoogleGPT
## Use Google's AI on discord, with highly customizable features.
Currently, the bot only supports the Gemini Pro model, with plans to gradually add other Google models in the future!.

https://github.com/FuseFairy/DiscordBot-GoogleGPT/assets/78064680/6420fa79-7c84-4d9c-8c2f-7405e49cca23
   
## Features
- **Gemini Pro Model:** The bot currently supports the Gemini Pro model for powerful AI interactions.
- **Customizable:** Highly customizable features to tailor the bot to your Discord server's needs.

<details>
   <summary>
   
   ### Slash command

   </summary>
   
* `/api_key setting [choice] [api_key]`
  * Can upload own google api key or delete it. (api key get from https://makersuite.google.com/app/apikey)
    * [choice]：`delete` or `set` your api key

  ![setting](https://i.imgur.com/QWcaGG6.png)
  
* `/character setting [prompt] [avatar] [name] [temperature] [harrassment] [hate_speech] [sexually_explicit] [dangerous_content]`
  * Can be used to customize a character or adjust some attributes on the model.
    * [prompt]：[click to see detail](https://ai.google.dev/docs/prompt_intro), go to Google AI Studio website to create new chat prompt, then write your prompt example, after finish, press `<> Get code` and copy and paste to `prompt`.

        ![prompt](https://i.imgur.com/lty9iHo.png)

        ![copy](https://i.imgur.com/PsVuAoh.png)

    * [avatar]：Upload your favorite character avatar.
    * [name]：Can set your character name.
    * [temperature]：Controls the level of randomness in the output, ranging from highly varied (closer to 1.0) to less surprising (closer to 0.0).
    * [harrassment]、[hate_speech]、[sexually_explicit]、[dangerous_content]：It's [Safety Settings](https://ai.google.dev/docs/safety_setting_gemini#safety-settings), the default is to Block some.

    ![create character](https://i.imgur.com/WybR2Ke.png)
  
* `/create conversation [model] [type] [use_prompt] [use_character]`
  * Create a thread exclusively for the user to chat with the bot.
    * [model]：Choose model.
    * [type]：Choose thread type, private or public.
    * [use_prompt]：Whether to use a prompt.
    * [use_character]：Enable it after you have set the 'name' and 'avatar' parameters using '/character setting'.

* `/reset conversation`
  * It will only clear the chat history, personalization settings will remain unchanged.
</details>

## Usage

### Install

```
pip install -r requirements.txt
```

### Discord bot permission

![permission](https://i.imgur.com/2uxDRA6.png)

### .env setting

```markdown
# Input your Discord bot token.
DISCORD_BOT_TOKEN=

# Can get from https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=

# Allow each commands only in specific channel, if you don't set it, just default to all channels.
# specific channel for /api_key setting
SETTING_CHANNEL_ID=

# specific channel for /create conversation
CHAT_CHANNEL_ID=

# specific channel for /reset conversation
RESET_CHAT_CHANNEL_ID=

# specific channel for /character setting
CHARACTER_CHANNEL_ID=

# specific channel for /help
HELP_CMD_CHANNEL_ID=
```

## Credits
* google-generativeai - [https://github.com/google/generative-ai-python](https://github.com/google/generative-ai-python)
