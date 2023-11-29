import metadata_parser


def get_information_from_link(link):
    try:
        page = metadata_parser.MetadataParser(url=link)
        metadata = page.metadata
        page_information = {
            'title': metadata.get('og').get('title') or metadata.get('page').get('title'),
            'description': metadata.get('og').get('description') or metadata.get('meta').get('description'),
            'link_type': metadata.get('og').get('type') or None,
            'image': metadata.get('og').get('image') or None,
        }

        return page_information
    except metadata_parser.NotParsableFetchError:
        return {}
