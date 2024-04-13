# Elephantlife
![image](https://github.com/Rishit-Gupta-RG/Elephantlife/assets/83908451/14fae009-0ab9-498a-b237-fa76762cc09d)

Elephantlife is a user-installable app written in [disnake](https://github.com/DisnakeDev/disnake), Discord [released](https://discord.com/developers/docs/change-log#userinstallable-apps-preview) a preview for user-installable apps on 18 March 2024. Elephantlife can create amazing GIFs using the [Jeyy API](https://api.jeyy.xyz/dashboard/).

# How to create a user-installable app?
1. Go to https://discord.com/developers/applications & create an application (or select an existing one).
2. Select "Installation" option from the left panel.

   ![image](https://github.com/Rishit-Gupta-RG/Elephantlife/assets/83908451/b8792ebe-b5ce-4c9b-ad0f-aeeb1df6c80f)
3. Check "User Install" option (you can also check "Guild Install" to make it work in servers as well.

   ![image](https://github.com/Rishit-Gupta-RG/Elephantlife/assets/83908451/e44d2858-0fb4-4251-a6ae-fa8e1be10daf)

4. Now you can add the bot using https://discord.com/oauth2/authorize?client_id=<your-bot's-application-id-here>.

# Running Locally
1. Install the requirements listed in [`requirements.txt`](https://github.com/Rishit-Gupta-RG/Elephantlife/blob/main/requirements.txt) file.
2. There are 2 variables:
   ```.env
   TOKEN =
   JEYY_API_KEY =
   ```
   Get your bot's `TOKEN` from https://discord.com/developers/applications.
   
   Get `JEYY_API_KEY` from https://api.jeyy.xyz/dashboard/.
3. Run `main.py`.

## Commands & features
`/gifmaker` - Upload an image to create a GIF

`Gif maker` (Context menu user command) - Create a GIF using the profile picture of the user directly

Can be used anywhere on discord (you must have permissions to use app commands in the channel where you want to use it)
