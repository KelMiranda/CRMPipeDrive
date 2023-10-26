from processes.deals import dictionary_invert

if __name__ == '__main__':
    #PipelineTable('pipeline').validator()
    #StageTable('stages').validator()
    #make_all_deals()
    print(dictionary_invert({'Open': 561, 'Closed': 562, 'Process': 563}, 561))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
