import telebot
import logging
import configparser
from telebot import types


class DialogBot:
    def __init__(self, is_logging=True):
        self.INTERNAL_CONFIG_PATH = "internal_config.ini"
        self.CONFIG_PATH = 'config.ini'
        self.TOKEN_PATH = 'token.ini'
        self.TOKEN = self.__get_token()

        self.bot = telebot.TeleBot(self.TOKEN);
        self.is_logging = self.__set_logging(is_logging)
        self.__set_up()

    def __get_token(self):
        token_config = configparser.ConfigParser()
        token_config.read(self.TOKEN_PATH)
        return token_config["DEFAULT"]["token"]

    def __set_logging(self, is_logging):
        self.is_logging = is_logging
        if is_logging:
            self.logger = telebot.logger
            telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

    def __update_params(self, settings):
        pass

    def __set_up_nn(self):
        pass

    def __get_settings(self, config_name, is_internal_config=False):

        settings_config = configparser.ConfigParser()
        if not is_internal_config:
            settings_config.read(self.CONFIG_PATH)
        else:
            settings_config.read(self.INTERNAL_CONFIG_PATH)
        print("settings configs", dict(settings_config))
        settings = dict(settings_config[str(config_name)])
        settings = {i: self.get_var_value(j) for (i, j) in settings.items()}
        return settings

    def __set_up(self):
        settings = self.__get_settings("DEFAULT")
        self.settings = settings
        self.__update_params(settings)
        self.__set_up_nn()
        self.__set_up_bot()

    def update_settings(self, config_name):
        settings = self.get_settings(configs)
        self.__update_params(settings)

    def get_settings(self, user_id='DEFAULT', is_internal_config=False):
        print(f'get_settings1 user_id: {user_id}')
        if not self.check_user_in_configs(user_id, is_internal_config=is_internal_config): user_id = "DEFAULT"
        print(f'get_settings2 user_id: {user_id}')
        return self.__get_settings(user_id, is_internal_config=is_internal_config)

    def __save_configs(self):
        pass

    def __save_settings(self, new_settings, user_id='DEFAULT', is_internal_config=False):  # for single config
        user_id = str(user_id)
        #      settings_config = configparser.ConfigParser()
        if not is_internal_config:
            fileway = self.CONFIG_PATH
        else:
            fileway = self.INTERNAL_CONFIG_PATH
        #        settings_config.read(fileway)
        #       settings_config[user_id] = new_settings
        # print(type(user_id),user_id,new_settings)
        settings_config = configparser.ConfigParser()
        settings_config.read(fileway)
        settings_config[user_id] = new_settings
        with open(fileway, 'w') as configfile:
            settings_config.write(configfile)

    def get_parameter(self, parameter_name, user_id="DEFAULT", is_internal_config=False):
        if not self.check_user_in_configs(user_id, is_internal_config=is_internal_config): user_id = "DEFAULT"
        return self.get_settings(user_id, is_internal_config=is_internal_config)[parameter_name]

    def update_parameter(self, parameter, new_value, user_id='DEFAULT', is_internal_config=False):
        settings = self.get_settings(user_id, is_internal_config)
        settings[parameter] = new_value
        self.__save_settings(settings, user_id, is_internal_config)

    def start(self, non_stop=True, interval=0, timeout=20):
        ''' После вызова этой функции TeleBot начинает опрашивать серверы Telegram на предмет новых сообщений.
        none_stop: True / False (по умолчанию False) - не прекращать опрос при получении ошибки от серверов Telegram

        interval: True / False (по умолчанию False) - интервал между запросами на опрос.
        изменение этого параметра снижает время отклика бота.

        timeout: целое число (по умолчанию 20) - Тайм-аут в секундах для длительного опроса
        '''
        self.bot.polling(non_stop=non_stop, interval=interval, timeout=timeout)
    def get_bot(self):
        return self.bot
    def set_to_default_config(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            "brightness": '0.5',
            'visibility': '0.5',

            # Цвета в HEX формате
            'color1': 'ecfc0a',  # желтый
            'color2': 'fad328',  # светло-оранжевый
            'color3': 'ff9000',  # темно-оранжевый
            'color4': 'fc0505',  # красный

            'auto_apply_changes': 'True',
            'return_separate_predict': 'False'
        }
        with open(self.CONFIG_PATH, 'w') as configfile:
            config.write(configfile)

    def set_to_default_internal_config(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'waiting_parameter': 'None',
            'username': 'None'
        }
        with open(self.INTERNAL_CONFIG_PATH, 'w') as configfile:
            config.write(configfile)

    def get_var_value(self, var: str):
        try:
            return float(var)
        except Exception as e:
            if var == 'True':
                return True
            elif var == 'False':
                return False
            else:
                return str(var)

    def get_user_id(self, message):
        return message.chat.id

    def __set_up_bot(self):
        bot = self.bot

        @bot.message_handler(commands=['start', 'help'])
        def send_usual_commands(message):
            if message.text == '/start':
                bot.reply_to(message, "Ok, lets start. To proccess photo enter: /draw. For extra info see /help")
            else:
                bot.reply_to(message,
                             "This bot transfer style image to content image. To set up content image run /set_content , for style image /set_style. To make tranfer run /draw")

        @bot.message_handler(commands=['set_up'])
        def send_settings(message):
            INSTRUCTION = "To update parameters press button on keyboard below."

            default_settings = self.get_settings(user_id=self.get_user_id(message))

            buttons_text = list(default_settings.keys())
            buttons_text.append("CANCEL")

            settings_str = ""
            for (key, item) in dict(default_settings).items():
                settings_str += f"{key}: \t{item}\n"

            keyboard = types.InlineKeyboardMarkup()

            for btn_txt in buttons_text:
                callback_button = types.InlineKeyboardButton(text=btn_txt, callback_data=btn_txt)
                keyboard.add(callback_button)

            bot.reply_to(message, f"Bot current settings:\n{settings_str}\n{INSTRUCTION}", reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            if call.message:
                user_id = self.get_user_id(call.message)  # call.message.from_user.id
                print(f'Recieve answer from user_id: {user_id}')
                username = call.message.from_user.username
                # print(call.data, list(self.settings.values()))
                if call.data in list(self.settings.keys()):
                    self.update_parameter("waiting_parameter", call.data, is_internal_config=True, user_id=user_id)
                    bot.send_message(call.message.chat.id, f"Changing {call.data}. Enter new value:")
                    bot.register_next_step_handler(call.message, update_settings_parameter);

                if call.data == "CANCEL":
                    self.update_parameter("waiting_parameter", "None", is_internal_config=True, user_id=user_id)
                    bot.send_message(call.message.chat.id, f"Action cancelled")

        # bot.register_next_step_handler(message, update_settings);


        # @bot.message_handler(content_types=['text'])
        # def get_unknown_message(message):
        #     bot.reply_to(message, "Unknown message. See /help command")
            # bot.reply_to(message, message.from_user.id)

        # def update_settings(message):

        def update_settings_parameter(message):
            user_id = self.get_user_id(message)  # message.from_user.id
            username = message.from_user.username
            if message.content_type == 'text':
                if message.text == '/cancel':
                    self.update_parameter("waiting_parameter", "None", is_internal_config=True, user_id=user_id)
                    bot.send_message(message.from_user.id, f"Command cancelled.")
                else:
                    waiting_parameter = self.get_parameter("waiting_parameter", is_internal_config=True,
                                                           user_id=user_id)
                    # print(waiting_parameter)
                    old_value = self.get_settings(user_id=user_id, is_internal_config=False)[waiting_parameter]
                    old_value_type = type(old_value)
                    new_value = self.get_var_value(message.text)
                    new_value_type = type(new_value)

                    if old_value_type != new_value_type:
                        bot.send_message(message.from_user.id,
                                         f"Thats wrong type. Please send correct, see original type above(to cancel send /cancel )")
                        bot.register_next_step_handler(message, update_settings_parameter);
                    else:
                        # message.from.id#message.from.username
                        if not self.check_user_in_configs(user_id, is_internal_config=True):
                            self.add_user_to_configs(user_id, username)
                            self.update_parameter("username", message.from_user.username, is_internal_config=True,
                                                    user_id=user_id)

                        self.update_parameter(waiting_parameter, new_value, user_id=user_id)  # Changing user params
                        self.update_parameter("waiting_parameter", "None", is_internal_config=True,
                                                user_id=user_id)  # Set waiting flag to none
                        bot.send_message(message.from_user.id, f"Got it. Parameter is changed")
            else:
                bot.send_message(message.from_user.id,
                                 f"Thats not a text type. Please send text(to cancel send /cancel )")
                bot.register_next_step_handler(message, update_settings_parameter);

        # @bot.message_handler(content_types=['photo'])
        # def get_image(message):
        #
        #     user_id = self.get_user_id(message)  # message.from_user.id
        #     if message.content_type == 'photo':
        #         raw = message.photo[-1].file_id  # max image size id
        #         path = raw + ".jpg"
        #         file_info = bot.get_file(raw)
        #         downloaded_file = bot.download_file(file_info.file_path)
        #         with open(path, 'wb') as new_file:
        #             new_file.write(downloaded_file)
        #
        #         bot.send_message(message.from_user.id, f"Got image. Please wait..")  # message.photo)
        #         # HERE IS PIC PROCCESSING
        #     elif message.text == '/cancel':
        #         bot.send_message(message.from_user.id, f"Canceling comand.")
        #         self.update_parameter("waiting_parameter", "None", is_internal_config=True, user_id=user_id)
        #     else:
        #         bot.send_message(message.from_user.id,
        #                          f"I cant read this Image or it's not image. Please send image(to cancel send /cancel )")
        #         bot.register_next_step_handler(message, get_image);

    def check_user_in_configs(self, user_id, is_internal_config=True):
        fileway = self.INTERNAL_CONFIG_PATH
        if not is_internal_config: fileway = self.CONFIG_PATH
        settings_config = configparser.ConfigParser()
        settings_config.read(fileway)
        all_configs = [i for (i, j) in
                       dict(settings_config).items()]  # {i:dict(j) for (i,j) in dict(settings_config).items()}
        print(all_configs, user_id)
        print(str(user_id) in all_configs)
        return str(user_id) in all_configs

    def add_user_to_configs(self, user_id, username):
        settings_config = configparser.ConfigParser()
        settings_config.read(self.CONFIG_PATH)
        settings_config[str(user_id)] = settings_config['DEFAULT']
        with open(self.CONFIG_PATH, 'w') as configfile:
            settings_config.write(configfile)

        settings_config = configparser.ConfigParser()
        settings_config.read(self.INTERNAL_CONFIG_PATH)
        settings_config[str(user_id)] = settings_config['DEFAULT']
        settings_config[str(user_id)]['username'] = username
        with open(self.INTERNAL_CONFIG_PATH, 'w') as configfile:
            settings_config.write(configfile)

        # pass#message.from_user.id#
        # message.from.id

        # message.from.username

if __name__ == '__main__':
    nnbot = DialogBot()
    nnbot.start()
