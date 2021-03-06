from pydub import AudioSegment
import os

#Contains the timestamps by page. Each page has a start and end timestamp which is used when splicing the chapter audio file
timeStamps = [
    [], #Leave here for proper indexing
    [[0, 46], [46, 110], [110, 167], [167.5, 207], [207, 244], [244, 273]], #C1
    [[0, 40], [40, 85], [85.25, 137], [137.5, 179], [179.5, 214], [214.5, 248.25], [248.5, 291.5], [292, 337], [337, 390.5], [391, 439.5], [439.5, 474], [474, 514], [514.5, 563.25], [563.75, 625.5], [625.5, 656.25], [656.5, 708.25], [708.5, 767]], #C2
    [[0, 44], [44, 95.75], [95.75, 140], [140, 195.5], [195.5, 227], [227, 275], [275, 328], [328, 378], [378, 413], [413, 449]], #C3
    [[0, 36.5], [36.5, 66.5], [66.5, 94.5], [94.5, 136], [136, 185], [185, 218.5], [218.5, 259.5], [259.5, 299], [299, 334], [334, 368.75], [368.75, 398], [398, 406]], #C4
    [[0, 36.5], [36.5, 72], [72, 113], [113, 150], [150, 189], [189, 223], [223, 262], [262, 305], [305, 338.5], [338.5, 369]], #C5 - Unfinished audio
    [[0, 48.5], [48.5, 89], [89, 128], [128, 162], [162, 213], [213, 254], [254, 287], [287, 321], [321, 363], [363, 395.5], [395.5, 434]], #C6
    [[0, 43], [43, 93.5], [93.5, 129], [129, 175], [175, 226], [226, 281], [281, 318.5], [318.5, 355.5], [355.5, 387], [387, 414.5], [414.5, 440.15], [440.15, 474], [474, 505], [505, 544], [544, 548]], #C7
    [[0, 58], [58, 89.75], [89.75, 146], [146, 190], [190, 228], [228, 277.5], [277.5, 326], [326, 387.5], [387.5, 431]], #C8
    [[0, 31], [31, 66], [66, 98.5], [98.5, 131], [131, 170], [170, 202], [202, 233.5], [233.5, 262], [262, 281]], #C9
    [[0, 58.5], [58.5, 98], [98, 131.5], [131.5, 162.5], [162.5, 193], [193, 225], [225, 268], [268, 315], [315, 362], [362, 404.5], [404.5, 452], [452, 493]], #C10
    [[0, 38], [38, 77.5], [77.5, 118], [118, 164.5], [164.5, 209], [209, 248.5], [248.5, 283.75]], #C11 - Unfinished audio
    [[0, 38.5], [38.7, 72.5], [73.8, 121.5], [122, 175], [175, 216], [216, 265], [265, 296], [296, 334.6], [334.8, 370], [370, 414.5], [415, 465.5], [465.7, 508], [508, 543.5], [543.7, 578.3], [578.5, 633.5], [633.7, 680], [680, 708]], #C12
    [[0, 49.3], [49.5, 91.5], [91.5, 128.2], [128.4, 180.5], [180.7, 218.3], [218.5, 266.2], [266.6, 309.3], [309.5, 340]], #C13
    [[0, 33], [33.5, 68], [68, 95.7], [95.9, 134], [134, 180], [180, 215], [215, 251.5], [252, 294.5], [294.8, 327]], #C14
    [[0, 40], [40, 88], [88, 136.5], [136.5, 172.5], [173, 207.5], [207.5, 245.5], [245.75, 276], [276.5, 308], [308.5, 346.5], [347, 389.5], [389.5, 436], [436.5, 487], [487.5, 497]], #C15
    [[0, 33], [33, 77], [77.5, 122], [122, 184.25], [184.5, 220], [220, 266], [266, 313.5], [314, 355.5], [355.75, 402]], #C16
    [[0, 40], [40, 78], [78.5, 106], [106, 157.5], [157.75, 197.5], [198, 222], [222.5, 257], [257, 294.5], [294.75, 326.5], [326.75, 364], [364, 408]], #C17
    [[0, 32], [32.5, 77.5], [78, 114.5], [115, 150.5], [151, 189.5], [190, 227.5], [228.25, 281.5], [281.75, 324.5], [325, 353]], #C18
    [[0, 34], [34, 74.3], [74.5, 121], [121, 153.5], [153.5, 198], [198, 226.5], [226.5, 264], [264, 307], [307, 342.5], [343, 386.45], [386.45, 427.75], [428, 471], [471, 493]], #C19
    [[0, 39], [39, 67], [68, 113.5], [113.5, 148], [148, 186], [186, 222], [223, 268], [268, 297], [297, 332], [332, 372.5], [372.5, 407]], #C20
    [[0, 48], [48, 88], [88, 133], [133, 177], [177, 215], [215, 253], [253, 274]] #C21
]

# Contains the starting page of each chapter
chapterStartPageNumber = [0, 1, 7, 24, 34, 46, 58, 69, 84, 93, 102, 114, 125, 142, 150, 159, 172, 181, 192, 209, 222, 233, 240]

# Method that splits chapter audio into pages. All chapter audio files (dd_1.mp3, dd_2.mp3, ..., dd_21.mp3) should be
# placed inside backend/Audio/ChapterAudio in order for the code below to run. Additionally, folders titled "C1", "C2", ...
# "C21" should be created within the ChapterAudio directory so all created audio files can be placed there.
def splitChapterAudioToPages():
    prefixPath = os.getcwd()
    newPath = os.path.abspath(os.path.join(prefixPath, os.pardir))
    chapterAudioDirectory = os.path.join(newPath, "Audio/ChapterAudio")
    files = os.listdir(chapterAudioDirectory)

    # Loop through each chapter and all pages within the chpater and splice chapter audio with the given timestamps
    for chapterNumber in range(1, 22):
        chapterAudioFile = "dd_" + str(chapterNumber) + ".mp3"
        pageNumber = chapterStartPageNumber[chapterNumber]
        if chapterAudioFile in files:
            chapterAudio = AudioSegment.from_mp3(chapterAudioDirectory + "/" + chapterAudioFile)
            pageTimeStamps = timeStamps[chapterNumber]
            for page in enumerate(pageTimeStamps):
                start = page[1][0] * 1000 # Works in milliseconds
                end = page[1][1] * 1000
                newAudio = chapterAudio[start:end] #Index chapterAudio file with start and end points
                filePath = chapterAudioDirectory + "/C" + str(chapterNumber) + "/Chapter"+ str(chapterNumber) + "_Page" + str(pageNumber) + ".mp3"

                newAudio.export(filePath, format="mp3") #Exports file "Chapter{chapterNum}_Page{pageNumber}.mp3" to specified file path
                pageNumber += 1

def main():
    splitChapterAudioToPages()

if __name__ == '__main__':
    main()
