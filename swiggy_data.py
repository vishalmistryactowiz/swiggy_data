import json

# This is  empty List
pro_data = []
base_path_img = "https://instamart-media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,h_600/" 
# load json data into python
def input_data(raw_data):
    with open(raw_data,"r") as f:
        data= json.load(f)
        return data
# process Python Date to acees
def praser(data):
    for card in data['data']['cards']:
        for item in card['card']['card']['gridElements']['infoWithStyle']['items']:
        
            for sub_item in item['variations']:
                product = dict()
                product['Product Name'] = sub_item['displayName']
                product['Product ID'] = sub_item['skuId']
                product['Product Price'] = float(sub_item['price']['offerPrice']["units"])
                product['Product quantity'] = sub_item['quantityDescription']
                product['Product Image Url'] = base_path_img + sub_item['imageIds'][0]
                product["Discount percentage"] = int(sub_item['price']['offerApplied']["listingDescription"].split('%')[0])
                product["Product MRP"] = float(sub_item['price']['mrp']['units'])
                product['Product In Stock'] = item['inStock']
                pro_data.append(product)
    return pro_data
# load python date to json           
def write_json(data):
    s = input("Enter New File Name:- ")
    with open(s,'w') as f:
        json.dump(data,f,indent=4)

# User Input
user_input = input("Emter a file Name:")
data =input_data(user_input)
alldata=praser(data)
write_json(alldata)
