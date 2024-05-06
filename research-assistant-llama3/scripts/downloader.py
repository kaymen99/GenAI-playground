from src.utils import get_papers_titles, download_multi_papers

# Reasearch topic
topic = "Machine learning"

# Number of research paper to download. You can adjust the limit as per your requirement
papers_count = 10

if __name__ == "__main__":
    papers_titles = get_papers_titles(topic, papers_count)
    print("Titles of papers related to ", topic)
    for title in papers_titles:
        print(title)

    download_multi_papers(papers_titles)