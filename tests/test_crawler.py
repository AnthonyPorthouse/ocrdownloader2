import os.path

from ocrdownloader2.crawler import get_track


def test_get_track(requests_mock):
    with open(os.path.dirname(__file__) + "/data/page_response.html") as body:
        requests_mock.get("https://ocremix.org/remix/OCR00000", text=body.read())

    track = get_track(0)

    assert track.id == 0
    assert track.title == 'The Legend of Zelda: Breath of the Wild "Torchlight"'
    assert track.checksum == "5753dc3e406eaf3d23887299961a14bc"
    assert track.links == {
        "https://iterations.org/files/music/remixes/Legend_of_Zelda_Breath_of_the_Wild_Torchlight_OC_ReMix.mp3",
        "https://ocrmirror.org/files/music/remixes/Legend_of_Zelda_Breath_of_the_Wild_Torchlight_OC_ReMix.mp3",
        "https://ocr.blueblue.fr/files/music/remixes/Legend_of_Zelda_Breath_of_the_Wild_Torchlight_OC_ReMix.mp3",
    }
