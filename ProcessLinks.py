"""
Removes all of the duplicate links from the idea_links.txt file.
Then saves the new list to a new file called idea_links_no_duplicates.txt
"""
import glob


def remove_duplicates():
    # get all of the files in the current dir that start with idea_links
    files = glob.glob('idea_links*.txt')
    all_ideas = []
    for filename in files:
        if filename == 'idea_links_no_duplicates.txt':
            continue
        with open(filename, 'r') as f:
            idea_links = f.readlines()
        idea_links = [link.strip() for link in idea_links]
        # remove any text at the end of any string starting with /messages
        idea_links = [link.split('/messages')[0] for link in idea_links]
        # There are a lot of duplicates in each set. So we'll remove them here and afterwards in case there is date overlap.
        idea_links = list(set(idea_links))
        all_ideas.extend(idea_links)
    idea_links = list(set(all_ideas))
    with open('idea_links_no_duplicates.txt', 'w') as f:
        for link in idea_links:
            f.write(link + '\n')


if __name__ == '__main__':
    remove_duplicates()