import face_recognition
import argparse
import time
import os
import re
from google_images_download import google_images_download

args_list = ["keywords", "keywords_from_file", "prefix_keywords", "suffix_keywords",
             "limit", "related_images", "format", "color", "color_type", "usage_rights", "size",
             "aspect_ratio", "type", "time", "time_range", "delay", "url", "single_image",
             "output_directory", "proxy", "similar_images", "specific_site", "print_urls", "print_size",
             "metadata", "extract_metadata", "socket_timeout", "thumbnail", "language", "prefix", "chromedriver","known_images_path"]

white_listed_image_formats = ['jpg','jpeg','png','gif','bmp']

def user_input():
    config = argparse.ArgumentParser()
    config.add_argument('-cf', '--config_file', help='config file name', default='', type=str, required=False)
    config.add_argument('-k', '--keywords', help='delimited list input', type=str, required=False)
    config.add_argument('-kf', '--keywords_from_file', help='extract list of keywords from a text file', type=str, required=False)
    config.add_argument('-sk', '--suffix_keywords', help='comma separated additional words added after to main keyword', type=str, required=False)
    config.add_argument('-pk', '--prefix_keywords', help='comma separated additional words added before main keyword', type=str, required=False)
    config.add_argument('-l', '--limit', help='delimited list input', type=str, required=False)
    config.add_argument('-f', '--format', help='download images with specific format', type=str, required=False,
                        choices=['jpg', 'gif', 'png', 'bmp', 'svg', 'webp', 'ico'])
    config.add_argument('-u', '--url', help='search with google image URL', type=str, required=False)
    config.add_argument('-x', '--single_image', help='downloading a single image from URL', type=str, required=False)
    config.add_argument('-o', '--output_directory', help='download images in a specific directory', type=str, required=False)
    config.add_argument('-d', '--delay', help='delay in seconds to wait between downloading two images', type=int, required=False)
    config.add_argument('-co', '--color', help='filter on color', type=str, required=False,
                        choices=['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown'])
    config.add_argument('-ct', '--color_type', help='filter on color', type=str, required=False,
                        choices=['full-color', 'black-and-white', 'transparent'])
    config.add_argument('-r', '--usage_rights', help='usage rights', type=str, required=False,
                        choices=['labeled-for-reuse-with-modifications','labeled-for-reuse','labeled-for-noncommercial-reuse-with-modification','labeled-for-nocommercial-reuse'])
    config.add_argument('-s', '--size', help='image size', type=str, required=False,
                        choices=['large','medium','icon','>400*300','>640*480','>800*600','>1024*768','>2MP','>4MP','>6MP','>8MP','>10MP','>12MP','>15MP','>20MP','>40MP','>70MP'])
    config.add_argument('-t', '--type', help='image type', type=str, required=False,
                        choices=['face','photo','clip-art','line-drawing','animated'])
    config.add_argument('-w', '--time', help='image age', type=str, required=False,
                        choices=['past-24-hours','past-7-days'])
    config.add_argument('-wr', '--time_range', help='time range for the age of the image. should be in the format {"time_min":"MM/DD/YYYY","time_max":"MM/DD/YYYY"}', type=str, required=False)
    config.add_argument('-a', '--aspect_ratio', help='comma separated additional words added to keywords', type=str, required=False,
                        choices=['tall', 'square', 'wide', 'panoramic'])
    config.add_argument('-si', '--similar_images', help='downloads images very similar to the image URL you provide', type=str, required=False)
    config.add_argument('-ss', '--specific_site', help='downloads images that are indexed from a specific website', type=str, required=False)
    config.add_argument('-p', '--print_urls', default=False, help="Print the URLs of the images", action="store_true")
    config.add_argument('-ps', '--print_size', default=False, help="Print the size of the images on disk", action="store_true")
    config.add_argument('-m', '--metadata', default=False, help="Print the metadata of the image", action="store_true")
    config.add_argument('-e', '--extract_metadata', default=False, help="Dumps all the logs into a text file", action="store_true")
    config.add_argument('-st', '--socket_timeout', default=False, help="Connection timeout waiting for the image to download", type=float)
    config.add_argument('-th', '--thumbnail', default=False, help="Downloads image thumbnail along with the actual image", action="store_true")
    config.add_argument('-la', '--language', default=False, help="Defines the language filter. The search results are authomatically returned in that language", type=str, required=False,
                        choices=['Arabic','Chinese (Simplified)','Chinese (Traditional)','Czech','Danish','Dutch','English','Estonian','Finnish','French','German','Greek','Hebrew','Hungarian','Icelandic','Italian','Japanese','Korean','Latvian','Lithuanian','Norwegian','Portuguese','Polish','Romanian','Russian','Spanish','Swedish','Turkish'])
    config.add_argument('-pr', '--prefix', default=False, help="A word that you would want to prefix in front of each image name", type=str, required=False)
    config.add_argument('-px', '--proxy', help='specify a proxy address and port', type=str, required=False)
    config.add_argument('-cd', '--chromedriver', help='specify the path to chromedriver executable in your local machine', type=str, required=False)
    config.add_argument('-ri', '--related_images', default=False, help="Downloads images that are similar to the keyword provided", action="store_true")
    config.add_argument('-kip', '--known_images_path', default=False, help="Please provide known images path")
    config_file_check = config.parse_known_args()
    object_check = vars(config_file_check[0])

    if object_check['config_file'] != '':
        records = []
        json_file = json.load(open(config_file_check[0].config_file))
        for record in range(0,len(json_file['Records'])):
            arguments = {}
            for i in args_list:
                arguments[i] = None
            for key, value in json_file['Records'][record].items():
                arguments[key] = value
            records.append(arguments)
        records_count = len(records)
    else:
        # Taking command line arguments from users
        args = config.parse_args()
        arguments = vars(args)
        records = []
        records.append(arguments)
    return records

class googlefacesearch(google_images_download.googleimagesdownload):
    
    def set_extra_attributes(self, arguments):
        print('Yeah its initializing')
        if arguments['known_images_path']:
            self.known_images_path = arguments['known_images_path']
            self.face_count = 0


    def initiate_download(self, arguments):
        self.set_extra_attributes(arguments)
        if arguments['single_image']:  # Download Single Image using a URL
            self.single_image(arguments['single_image'])
        else:  # or download multiple images based on keywords/keyphrase search
            t0 = time.time()  # start the timer
            self.download(arguments)

            print("\nEverything downloaded!")
            t1 = time.time()  # stop the timer
            total_time = t1 - t0  # Calculating the total time required to crawl, find and download all the links of 60,000 images
            print("Total time taken: " + str(total_time) + " Seconds")

    def _get_all_items(self,page,main_directory,dir_name,limit,arguments):
        if self.known_images_path:
            self.known_face_names = []
            self.known_face_encodings = []
            for image in os.listdir(self.known_images_path):
                # Load the picture
                loaded_image = face_recognition.load_image_file("{}/{}".format(self.known_images_path,image))
                # Get facial encodings
                face_encoding = face_recognition.face_encodings(loaded_image)[0]
                self.known_face_names.append(image.split('.')[0])
                self.known_face_encodings.append(face_encoding)
        else:
            return
        items = []
        errorCount = 0
        i = 0
        count = 1
        total_count = 1
        while count < limit+1:
            object, end_content = self._get_next_item(page)
            if object == "no_links":
                break
            elif object == "":
                page = page[end_content:]
            else:
                #format the item for readability
                object = self.format_object(object)
                if arguments['metadata']:
                    print("\nImage Metadata: " + str(object))

                items.append(object)  # Append all the links in the list named 'Links'

                #download the images
                download_status,download_message,return_image_name = self.download_image(object['image_link'],object['image_format'],main_directory,dir_name,count,arguments['print_urls'],arguments['socket_timeout'],arguments['prefix'],arguments['print_size'])
                print(download_message)
                if download_status == "success":

                    # download image_thumbnails
                    if arguments['thumbnail']:
                        download_status, download_message_thumbnail = self.download_image_thumbnail(object['image_thumbnail_url'],main_directory,dir_name,return_image_name,arguments['print_urls'],arguments['socket_timeout'],arguments['print_size'])
                        print(download_message_thumbnail)                    
                    count += 1
                    total_count += 1

                    # check if downloaded image has a known face
                    filename = main_directory + '/' + dir_name + '/' + return_image_name
                    frame = face_recognition.load_image_file(filename)
                    rgb_frame = frame[:, :, ::-1]

                    face_locations = face_recognition.face_locations(rgb_frame)
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    # Initialize a empty array
                    face_names = []
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                        name = "Unknown"
                        # If a match was found in known_face_encodings, just use the first one.
                        if True in matches:
                            # first_match_index = matches.index(True)
                            # name = self.known_face_names[first_match_index]
                            self.face_count += 1
                else:
                    errorCount += 1

                #delay param
                if arguments['delay']:
                    time.sleep(int(arguments['delay']))

                page = page[end_content:]
            i += 1
            if count == limit+1:
                # for face_name in self.known_face_names:
                    print("Downloaded {} images out of which {} are from known faces".format(total_count-1,self.face_count))
                    user_decision = input("Do you want to search in more images?. (Yes/No)").lower().strip()
                    if user_decision == 'yes' or user_decision == 'y':
                        new_limit = input("Please Enter the new limit")
                        try:
                            new_limit = int(new_limit)
                            limit += new_limit
                        except:
                            print('Aborting because the value entered is not an integer')


        if count < limit:
            print("\n\nUnfortunately all " + str(
                limit) + " could not be downloaded because some images were not downloadable. " + str(
                count-1) + " is all we got for this search filter!")
            print("Downloaded {} images out of which {} are from known faces".format(count-1,self.face_count))
        return items,errorCount

    #function to download single image
    def single_image(self,image_url):
        main_directory = "downloads"
        url = image_url
        try:
            os.makedirs(main_directory)
        except OSError as e:
            if e.errno != 17:
                raise
            pass
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
        response = urlopen(req, None, 10)
        image_name = str(url[(url.rfind('/')) + 1:])
        if '?' in image_name:
            image_name = image_name[:image_name.find('?')]
        if ".jpg" in image_name or ".gif" in image_name or ".png" in image_name or ".bmp" in image_name or ".svg" in image_name or ".webp" in image_name or ".ico" in image_name:
            output_file = open(main_directory + "/" + image_name, 'wb')
        else:
            output_file = open(main_directory + "/" + image_name + ".jpg", 'wb')
            image_name = image_name + ".jpg"

        data = response.read()
        output_file.write(data)
        response.close()
        print("completed ====> " + image_name)
        return


def check_if_known_images_path_contains_images(known_images_path):
    return_val = ''
    if not os.path.exists(known_images_path):
        print("{} directory doesn't exist".format(known_images_path))
        return return_val

    files = os.listdir(known_images_path)
    if not len(files):
        print("{} directory doesn't contain any images".format(known_images_path))
    else:
        if not len(re.findall('|'.join(white_listed_image_formats),''.join(files))):
            print("Please use one of the file extensions of images {}".format(','.join(white_listed_image_formats)))
        else:
            return_val = known_images_path
    return return_val

#------------- Main Program -------------#
def main():
    records = user_input()
    for arguments in records:
        
        if not arguments['known_images_path']:
            arguments['known_images_path'] = 'images'
        kip_return_val = check_if_known_images_path_contains_images(arguments['known_images_path'])
        if not kip_return_val:
            break
        else:
            arguments['known_images_path'] = kip_return_val

        gfs_response = googlefacesearch()

        gfs_response.initiate_download(arguments)
        

if __name__ == "__main__":
    main()





