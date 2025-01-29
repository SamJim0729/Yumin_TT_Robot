import os
import sys
import boto3
from botocore.exceptions import NoCredentialsError
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config'))
from config.config import Config
from linebot.v3.messaging.models import ImageCarouselTemplate, ImageCarouselColumn,LocationMessage, CarouselTemplate, CarouselColumn,  URIAction, PostbackAction, TemplateMessage, ButtonsTemplate, URIAction


BUCKET_NAME = os.getenv('BUCKET_NAME', 'yumin-tt-robot-photos')
REGION_NAME = os.getenv('AWS_REGION', 'ap-northeast-1')

s3_client = boto3.client('s3', region_name=REGION_NAME)

def generate_presigned_url(object_key, expiration=3600):
    """
    生成 S3 預簽名 URL
    :param object_key: S3 中的物件鍵（文件路徑）
    :param expiration: URL 有效時間（秒）
    :return: 預簽名 URL
    """
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_key},
            ExpiresIn=expiration
        )
        return url
    except NoCredentialsError:
        raise Exception("AWS credentials not available")
    except Exception as e:
        raise Exception(f"Failed to generate presigned URL: {e}")


def main_menu_view():
    """
    生成主選單視圖，包括課程資訊與球館資訊
    :return: TemplateMessage（主選單模板）
    """
    main_template_1_url = generate_presigned_url('images/mian_template_1.png')
    main_template_2_url = generate_presigned_url('images/mian_template_2.png')

    return TemplateMessage(
            alt_text='main_menu_view',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=main_template_1_url,
                        title='裕民國小桌球室',
                        text='課程資訊',
                        actions=[
                            PostbackAction(
                                label='團體課程', #
                                display_text='團體課程介紹', #回傳顯示文字
                                data='團體課(input)' #真正傳送資料
                            ),

                            PostbackAction(
                                label='個人課程', #
                                display_text='個人課程介紹', #回傳顯示文字
                                data='個人課(input)' #真正傳送資料
                            ),

                            PostbackAction(
                                label='租桌零打',
                                display_text='租桌零打介紹', #顯示文字
                                data='租桌零打(input)' #真正傳送資料
                            )
                        ]
                    ),

                    CarouselColumn(
                        thumbnail_image_url=main_template_2_url,
                        title='裕民國小桌球室',
                        text='球館資訊',
                        actions=[
                            PostbackAction(
                                label='營業時間',
                                display_text='🈺週一~週五:18:30-22:00\n🈺週六~週日: 8:30-18:00', #顯示文字
                                data='營業時間(input)' #真正傳送資料
                            ),

                            PostbackAction(
                                label='球場位置',
                                #display_text='🏫新北市新莊區裕民街123號（側門龍安路上)', #顯示文字
                                data='球場位置(input)' #真正傳送資料
                            ),

                            PostbackAction(
                                label='場地介紹',
                                display_text='👍場地寬敞、冷氣開放、5mm全新地墊、ITTF認證球桌',
                                data='場地介紹(input)' #真正傳送資料
                            )
                        ]
                    ),
                ]
            )
        )

def get_location_message_view():
    """
    生成地理位置訊息，提供球館地址與地圖
    :return: LocationMessage（地理位置信息）
    """
    return LocationMessage(
        title='新北市新莊區裕民國民小學',
        address='🏫新北市新莊區裕民街123之1號（側門龍安路上)',
        latitude=25.020637906844836,
        longitude=121.41826196401571
    )

def group_class_main_view():
    """
    團體課資訊模板，包含費用與課程時間
    :return: TemplateMessage（團體課模板）
    """
    group_template_url = generate_presigned_url("images/group_template.png")

    return TemplateMessage(
            alt_text='group_class_view',
            template=ButtonsTemplate(
                thumbnail_image_url=group_template_url,
                title='團體課資訊',
                text='查詢資訊或留下聯絡方式專人回覆',
                actions=[
                    PostbackAction(
                        label='費用說明', 
                        display_text='🪙費用:450/堂\n🔉說明:1.5hr/堂，每班3-6同學',
                        data='團體課費用(input)' #真正傳送資料
                    ),

                    PostbackAction(
                        label='開課班段', 
                        display_text='🕖週一~週五:\n    ALL 19:00-20:30\n🕘週六~週日:\n    A班 09:00-10:30\n    B班 10:40-12:10\n    C班 13:30-15:00\n    D班 15:10-16:40', 
                        data='團體課班段(input)' #真正傳送資料
                    ),

                    URIAction(
                        label='留下聯絡資訊',
                        uri='https://forms.gle/cU2TGo6LiVEAK6Ln7'
                    ),
                ]
            )
        )

def one_on_one_class_main_view():
    """
    個人課資訊模板，包含費用與注意事項
    :return: TemplateMessage（個人課模板）
    """
    one_on_one_template_url = generate_presigned_url("images/one_on_one_template.png")
    
    return TemplateMessage(
            alt_text='one_on_one_class_main_view',
            template=ButtonsTemplate(
                thumbnail_image_url=one_on_one_template_url, #確認一下圖片比例，做漸層
                title='個人課資訊',
                text='查詢資訊或留下聯絡方式專人回覆',
                actions=[
                    PostbackAction(
                        label='費用說明', 
                        display_text='1️⃣C級教練:850元/hr\n2️⃣B級教練:1,000元/hr\n3️⃣A級教練:1,100元/hr',
                        data='個人課費用(input)' #真正傳送資料
                    ),

                    PostbackAction(
                        label='補充說明', 
                        display_text='🔉若有15青、17青、19青、成人國手教練需求，費用請另洽櫃台\n📅個別課上課時間需與教練討論確認', 
                        data='個人課補充說明(input)' #真正傳送資料
                    ),

                    URIAction(
                        label='留下聯絡資訊',
                        uri='https://forms.gle/cU2TGo6LiVEAK6Ln7'##############################################
                            ),
                ]
            )
        )

def casual_play_main_view():
    """
    生成租桌零打資訊的模板
    :return: TemplateMessage（租桌零打資訊模板）
    """
    casual_play_template_url = generate_presigned_url("images/casual_play_template.png")
    return TemplateMessage(
            alt_text='casual_play_view',
            template=ButtonsTemplate(
                thumbnail_image_url=casual_play_template_url, #確認一下圖片比例，做漸層
                title='租桌零打資訊',
                text='查詢資訊',
                actions=[
                    PostbackAction(
                        label='費用說明', #
                        display_text='🏓球桌:200/hr\n🙋人頭:150/次(2.5hr)', #回傳顯示文字
                        data='租桌零打費用(input)' #真正傳送資料
                    ),

                    PostbackAction(
                        label='補充說明', 
                        display_text='🔉本場地有提供單球(無提供多球)、但無提供球拍',
                        data='租桌零打補充說明(input)'
                    )
                ]
            )
        )

def get_court_photos_view():
    """
    球場照片輪播模板
    :return: TemplateMessage（照片輪播模板）
    """
    court_photo_1_url = generate_presigned_url("images/court_photo_1.jpg")
    court_photo_2_url = generate_presigned_url("images/court_photo_2.jpg")
    court_photo_3_url = generate_presigned_url("images/court_photo_3.jpg")

    return TemplateMessage(
            alt_text='get_court_photos_view',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=court_photo_1_url,
                        action=PostbackAction(
                        label="photo_1",
                        data="球場照片1(input)" 
                    )),
                    ImageCarouselColumn(
                        image_url=court_photo_2_url,
                        action=PostbackAction(
                        label="photo_2",
                        data="球場照片2(input)" 
                    )),
                    ImageCarouselColumn(
                        image_url=court_photo_3_url,
                        action=PostbackAction(
                        label="photo_3",
                        data="球場照片3(input)"
                    )),
                    ]
                )
            )


    

