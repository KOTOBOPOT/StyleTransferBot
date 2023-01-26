from bot import DialogBot
import files_proccessing
import ImagesProcessing
from PIL import Image

import os

class StyleTransferBot(DialogBot):
    USERS_WAY = "C:/Users/boris/OneDrive/Рабочий стол/1 учеба/ML/Deep Learning School 1-ый семестр/проект/StyleTransfer/users/"
    RES_WAY= "C:/Users/boris/OneDrive/Рабочий стол/1 учеба/ML/Deep Learning School 1-ый семестр/проект/StyleTransfer/results/"

    def __init__(self, save_images = False):
        super().__init__(is_logging= True)
        self.__set_up_image_bot()
        self.SAVE_IMAGES = save_images
        self.Network = ImagesProcessing.StyleNet()

    def __set_up_image_bot(self):
        bot = self.bot

        #@bot.message_handler(content_types=('photo'))
        #def photo_pr(message):
        #    bot.reply_to(message, "Got  images to process..")
        #            
#        #            bot.register_next_step_handler(message, get_content_image);

        @bot.message_handler(commands=['draw'])
        def send_processing(message):
            user_id = str(self.get_user_id(message))
            if not files_proccessing.is_file_in_user_folder(user_id, "style.jpg"):
                bot.reply_to(message, "You haven't sent style image. Run /set_style command")
            elif not files_proccessing.is_file_in_user_folder(user_id, "content.jpg"):
                bot.reply_to(message, "You haven't sent content image. Run /set_content command")
            else:      
                bot.reply_to(message, "Please wait....")
                user_fileway = files_proccessing.get_user_fileway(user_id)
                self.Network.run(f'{user_fileway}/content.jpg',f'{user_fileway}/style.jpg', user_fileway,3)
                bot.send_photo(user_id, photo=open(files_proccessing.get_user_fileway(user_id)+ '/res.jpg', 'rb'))

                style_image = Image.open(files_proccessing.USERS_WAY + f'{user_id}/style.jpg')
                content_image = Image.open(files_proccessing.USERS_WAY + f'{user_id}/content.jpg')
                res_image = Image.open(files_proccessing.USERS_WAY + f'{user_id}/res.jpg')
                path = files_proccessing.create_res_folder()
                style_image.save(path +'/style.jpg' )
                content_image.save(path +'/content.jpg' )
                res_image.save(path + '/res.jpg')

        @bot.message_handler(commands=['set_content'])
        def get_set_content_command(message):
            bot.register_next_step_handler(message, get_content_image);
            bot.reply_to(message, "Send content image: ")
        def get_content_image(message):
            user_id = self.get_user_id(message)  # message.from_user.id
            if message.content_type == 'photo':
                raw = message.photo[-1].file_id  # max image size id
                path = files_proccessing.create_user_folder(user_id) + "/" + 'content' + ".jpg"
                file_info = bot.get_file(raw)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(path, 'wb') as new_file:
                    new_file.write(downloaded_file)

                bot.send_message(message.from_user.id, f"Got content image")  # message.photo)
               # bot.register_next_step_handler(message, get_style_image);# HERE IS PIC PROCCESSING
            elif message.text == '/cancel':
                bot.send_message(message.from_user.id, f"Canceling comand.")
                self.update_parameter("waiting_parameter", "None", is_internal_config=True, user_id=user_id)
            else:
                bot.send_message(message.from_user.id,
                                 f"I cant read this Image or it's not image. Please send image(to cancel send /cancel )")
                bot.register_next_step_handler(message, get_content_image);    
        @bot.message_handler(commands=['set_style'])
        def get_set_style_command(message):
            bot.reply_to(message, "Send style image: ")
            bot.register_next_step_handler(message, get_style_image);
        def get_style_image(message):
            user_id = self.get_user_id(message)  # message.from_user.id
            if message.content_type == 'photo':
            
                raw = message.photo[-1].file_id  # max image size id
                path = files_proccessing.create_user_folder(user_id) + "/" + 'style' + ".jpg"
                file_info = bot.get_file(raw)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(path, 'wb') as new_file:
                    new_file.write(downloaded_file)

                bot.send_message(message.from_user.id, f"Got style image.")  # message.photo)
                
            elif message.text == '/cancel':
                bot.send_message(message.from_user.id, f"Canceling comand.")
                self.update_parameter("waiting_parameter", "None", is_internal_config=True, user_id=user_id)
            else:
                bot.send_message(message.from_user.id,
                                 f"I cant read this Image or it's not image. Please send image(to cancel send /cancel )")
                bot.register_next_step_handler(message, get_style_image);

        @bot.message_handler(content_types=['text'])
        def get_unknown_message(message):
            bot.reply_to(message, "Unknown message. See /help command")
if __name__ == '__main__':
    bot = StyleTransferBot()
    bot.start()
    #print(2)