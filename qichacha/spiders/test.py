def process():
    file_path = "/Users/liebaomac/customer_company_extended_info_from_qichacha"
    with open(file_path) as fp:
        for line in fp:
            line = line.strip().split("\t")
            if line[14] == "":
                new_item = "0"
            else:
                new_item = str(len(line[14].split("+")))
            print "\t".join(line[:14] + [new_item] + line[15:])

process()

