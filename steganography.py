from stegano import lsb

origin_image = "origin.png"
output_image = "output.png"

secret = "Hello world! This is a test of the information hiding feature of the chat system"


def encode_image(origin_image, output_image, secret):
    encoded = lsb.hide(origin_image, secret)
    encoded.save(output_image)


def decode_image(encoded_image):
    print(lsb.reveal(output_image))


encode_image(origin_image, output_image, secret)
decode_image(output_image)
