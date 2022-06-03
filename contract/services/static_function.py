from decouple import config


def get_company_image(link):
    return f"""
        <img style="position:absolute; top:20px; right:35px;" width="350" height="150" src="{config('HOST')}:{config('PORT')}{link}"  alt="" >
    """


def get_company_image_link(link):
    return f"{config('HOST')}:{config('PORT')}{link}"
