import xml.etree.ElementTree as ET

def find_duplicates(root):
    seen = {}
    duplicates = []

    for question in root.findall('question'):
        name_element = question.find('name')
        questiontext_element = question.find('questiontext')

        if name_element is not None and questiontext_element is not None:
            name_text_element = name_element.find('text')
            questiontext_text_element = questiontext_element.find('text')

            if name_text_element is not None and questiontext_text_element is not None:
                name = name_text_element.text
                questiontext = questiontext_text_element.text

                key = (name, questiontext)
                if key in seen:
                    duplicates.append(question)
                else:
                    seen[key] = question

    return duplicates

def remove_duplicates(root, duplicates):
    for question in duplicates:
        root.remove(question)

def find_questions_with_video(root):
    questions_with_video = []
    for question in root.findall('question'):
        questiontext_element = question.find('questiontext')
        if questiontext_element is not None:
            questiontext_text_element = questiontext_element.find('text')
            if questiontext_text_element is not None and 'video controls="true"' in questiontext_text_element.text:
                questions_with_video.append(question)
    return questions_with_video

def remove_questions_with_video(root, questions_with_video):
    for question in questions_with_video:
        root.remove(question)

def main():
    tree = ET.parse('questions_m4.xml')
    root = tree.getroot()

    duplicates = find_duplicates(root)
    print(f"Found {len(duplicates)} duplicate questions.")
    remove_duplicates(root, duplicates)

    questions_with_video = find_questions_with_video(root)
    print(f"Found {len(questions_with_video)} questions with video.")
    remove_questions_with_video(root, questions_with_video)

    # Save questions with video
    video_tree = ET.ElementTree(ET.Element('questions'))
    video_tree.getroot().extend(questions_with_video)
    video_tree.write('questions_with_video.xml', encoding='utf-8', xml_declaration=True)
    print("Questions with video saved as 'questions_with_video.xml'.")

    # Save cleaned XML
    tree.write('questions_m4_cleaned.xml', encoding='utf-8', xml_declaration=True)
    print("Cleaned XML saved as 'questions_m4_cleaned.xml' with UTF-8 encoding.")

if __name__ == "__main__":
    main()

