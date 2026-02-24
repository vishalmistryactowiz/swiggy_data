import json
import mysql.connector

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="actowiz",
  database="swiggy"
)
cursor = conn.cursor()
def create_tables(cursor):
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id VARCHAR(25) ,
        product_name VARCHAR(255) NOT NULL,
        description TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_variants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(25),   -- FIXED
    quantity_description VARCHAR(100),
    price DECIMAL(10,2),
    mrp DECIMAL(10,2)
);
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_images (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id VARCHAR(25),
        image_url TEXT
    );
    """)
create_tables(cursor)
conn.commit()
    

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
                product['Product Image Url'] =  sub_item['imageIds']
                product['Product Image Url'] = [base_path_img+image for image in product['Product Image Url']]
                product["Discount percentage"] = int(sub_item['price']['offerApplied']["listingDescription"].split('%')[0])
                product["Product MRP"] = float(sub_item['price']['mrp']['units'])
                product['Product In Stock'] = item['inStock']
                product["Product Description"] = sub_item["shortDescription"]
                pro_data.append(product)

    # data.cards[0].card.card.gridElements.infoWithStyle.items[0].variations[0].shortDescription
    return pro_data
# load python date to json           
def write_json(data):
    s = input("Enter New File Name:- ")
    with open(s,'w') as f:
        json.dump(data,f,indent=4)
def insert_data(cursor, products):

    inserted_products = {}

    for item in products:

        product_id = item['Product ID']
        product_name = item['Product Name']

        if product_id not in inserted_products:

            # Insert product
            cursor.execute("""
                INSERT INTO products (product_id, product_name, description)
                VALUES (%s, %s, %s)
            """, (
                product_id,
                product_name,
                item.get('Product Description')
            ))

            inserted_products[product_id] = True

            # Insert images
            for image in item['Product Image Url']:
                cursor.execute("""
                    INSERT INTO product_images (product_id, image_url)
                    VALUES (%s, %s)
                """, (product_id, image))

        # Insert variant
        cursor.execute("""
            INSERT INTO product_variants 
            (product_id, quantity_description, price, mrp)
            VALUES (%s, %s, %s, %s)
        """, (
            product_id,
            item['Product quantity'],
            item['Product Price'],
            item['Product MRP']
        ))
# User Input
user_input = input("Emter a file Name:")
data =input_data(user_input)
alldata=praser(data)
insert_data(cursor, alldata)
conn.commit()
write_json(alldata)
conn.close()