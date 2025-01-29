from langchain.tools import StructuredTool

"""
定義球館的基本資訊函數，回傳固定的字典格式
"""

def get_opening_hours() -> dict:
    return {
    "週一至週五": "18:30-22:00",
    "週六至週日": "08:30-18:00"
}

def get_court_address() -> dict:
    return {
    "地址": "新北市新莊區裕民街123之1號（側門龍安路上)"
}

def get_contact_info() -> dict:
    return {
    "聯絡資訊": "https://forms.gle/cU2TGo6LiVEAK6Ln7"
}

def get_group_class_schedule() -> dict:
    return {
    "週一至週五": "19:00-20:30",
    "週六-週日": {
        "A班": "09:00-10:30",
        "B班": "10:40-12:10",
        "C班": "13:30-15:00",
        "D班": "15:10-16:40"
    }
}

def get_group_class_fee() -> dict:
    return {
    "團課費用": "450/堂",
    "補充說明": "1.5hr/堂，每班3-6同學",
    "注意事項": "實際報價仍以櫃檯報價為準"
}

def get_individual_class_fee() -> dict:
    return {
    "C級教練": "一小時 850元",
    "B級教練": "一小時1,000元",
    "A級教練": "一小時1,100元",
    "國手教練": "請洽櫃檯",
    "注意事項": "實際報價仍以櫃檯報價為準"
}

def get_rental_fee() -> dict:
    return {
    "球桌租借費用": "🏓球桌:200/hr",
    "每位人頭費用": "🙋人頭:150/次(2.5hr)"
}


def available_tools() -> list:
    """
    註冊所有可供 AI 使用的工具 (StructuredTool)
    :return: StructuredTool 工具列表
    """
    get_opening_hours_tool = StructuredTool.from_function(
        func=get_opening_hours,
        name='get_opening_hours',
        description='球場營業時間',
    )

    get_court_address_tool = StructuredTool.from_function(
        func=get_court_address,
        name='get_court_address',
        description='球場地址位置',
    )

    get_contact_info_tool = StructuredTool.from_function(
        func=get_contact_info,
        name='get_contact_info',
        description='有興趣想填表留下聯絡資訊，或是想連絡球館負責人，都提供此功能',
    )

    get_group_class_schedule_tool = StructuredTool.from_function(
        func=get_group_class_schedule,
        name='get_group_class_schedule',
        description='團體課開課時間',
    )

    get_group_class_fee_tool = StructuredTool.from_function(
        func=get_group_class_fee,
        name='get_group_class_fee',
        description='團體課費用說明，包含每堂上課時間，上課人數說明',
    )

    get_individual_class_fee_tool = StructuredTool.from_function(
        func=get_individual_class_fee,
        name='get_individual_class_fee',
        description='個人課費用費用說明',
    )

    get_rental_fee_tool = StructuredTool.from_function(
        func=get_rental_fee,
        name='get_rental_fee',
        description='租桌零打費用說明',
    )

    return [get_opening_hours_tool, get_court_address_tool, get_contact_info_tool, get_group_class_schedule_tool, get_group_class_fee_tool, get_individual_class_fee_tool, get_rental_fee_tool]

