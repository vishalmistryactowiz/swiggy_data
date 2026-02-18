import json

pro_item = []
base_path_img = "https://instamart-media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,h_600/" 
# load json data into python
def input_data(raw_data):
    with open(raw_data,"r") as f:
        data= json.load(f)
        return data
    
# process Python Date to acees
def praser(data):
    for card in data['data']['cards']:
        card_item = card.get("card",{}).get("card",{}).get("gridElements",{}).get("infoWithStyle",{}).get("items",{})
        for item in card_item:
            for sub_item in item['variations']:
                product= {
                'Product Name':sub_item.get('displayName'),
                'Product ID':sub_item.get('skuId'),
                'Product Price':float(sub_item['price']['offerPrice']["units"]),
                'Product quantity': sub_item.get('quantityDescription'),
                'Product Image Url': sub_item.get('imageIds'),
                'Product Image Url': [base_path_img+image for image in sub_item["imageIds"]],
                "Discount percentage" : int(sub_item['price']['offerApplied']["listingDescription"].split('%')[0] or 0),
                "Product MRP" :float(sub_item['price']['mrp']['units']),
                'Product In Stock' :item['inStock']
                }
            pro_item.append(product)
    return pro_item
    
# load python date to json           
def write_json(data):
    file_user_input= input("Enter New File Name:- ")
    with open(file_user_input,'w') as f:
        json.dump(data,f,indent=4)

# User Input
user_input = input("Emter a file Name:")
data =input_data(user_input)
alldata=praser(data)
write_json(alldata)
