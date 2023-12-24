import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

# Load data
@st.cache_data
def load_data():
    sample = Path(__file__).resolve().parent / "assets" / "sample.csv"
    return pd.read_csv(sample)

# Calculate similarity
def calculate_similarity(data):
    # Combine Title, Description, and Category into a single string
    data['Combined'] = data['Title'] + ' ' + data['Description'] + ' ' + data['Category']

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['Combined'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def main():
    st.title('Product Similarity Analyzer')
    st.write("""This app analyzes the similarity between products in the Product Search Corpus dataset.
             To begin, choose a product from the left dropdown menu to serve as the basis for the similarity comparison. 
             Afterwards, a list of products with the highest similarity to your selected product will be displayed below.
             """)

    # Load data
    data = load_data()

    # Calculate similarity
    similarity_matrix = calculate_similarity(data)

    # Streamlit sidebar
    st.sidebar.header('Select a Product')
    selected_product = st.sidebar.selectbox('Choose a product', data['Title'])

    # Display similar products
    st.subheader(f"Products similar to: {selected_product}:")
    product_index = data[data['Title'] == selected_product].index[0]
    similar_products = list(enumerate(similarity_matrix[product_index]))
    similar_products = sorted(similar_products, key=lambda x: x[1], reverse=True)[1:6]

    # Calculate total similarity scores for each category
    category_names = data['Category'].unique()
    total_similarity_by_category = {category: 0 for category in category_names}

    for index, score in similar_products:
        category = data['Category'].iloc[index]
        total_similarity_by_category[category] += score

    # Find the category with the highest total similarity score
    max_similarity_category = max(total_similarity_by_category, key=total_similarity_by_category.get)

    # Display the category with the most products with similarity
    st.write(f"Category with Most Products Similar: {max_similarity_category}")

    for i, (index, score) in enumerate(similar_products, 1):
        st.write(f"{i}. {data['Title'].iloc[index]} (Similarity Score: {score:.2f})")

    # Interactive Scatter Plot for Similarity Scores
    st.subheader('Interactive Scatter Plot for Similarity Scores')
    selected_product_similarity = similarity_matrix[product_index]
        
    source = ColumnDataSource(data=dict(
        x=range(len(selected_product_similarity)),
        y=selected_product_similarity,
        names=data['Title'],
        categories=data['Category']
    ))

    hover = HoverTool(tooltips=[("Product", "@names"), ("Category", "@categories")])

    p = figure(title='Similarity Scores with Other Products', x_axis_label='Product Index', y_axis_label='Similarity Score', tools=[hover])
    p.scatter('x', 'y', size=8, color='navy', source=source)

    st.bokeh_chart(p, use_container_width=True)

if __name__ == '__main__':
    main()
