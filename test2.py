import rpa

def main():
    img1 = "img/add_icon.JPG"
    img2 = "img/subflow_icon.JPG"
    
    imgsRenameSubflow = [
        "img/rename-subflow-txt.jpg",
        "img/subflow-name-txt.jpg"
    ]

    rpa.waitAppearAny(imgsRenameSubflow)

if __name__ == "__main__":
    main()
