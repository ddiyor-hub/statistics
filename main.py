import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

# Configuration
st.set_page_config(page_title="Advanced Stats App", layout="wide", page_icon="📊")

# Custom Matplotlib style
plt.style.use('ggplot')

# Cache data loading
@st.cache_data
def load_data(uploaded_file):
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Main app
def main():
    st.title("📊 Advanced Statistical Analysis Tool")
    
    # File upload with validation
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"], 
                                           help="Upload a dataset with numerical columns")
    
    if not uploaded_file:
        st.info("Please upload a CSV file to begin analysis")
        return

    # Load data with error handling
    df = load_data(uploaded_file)
    if df is None or df.empty:
        st.error("Invalid or empty file. Please upload a valid CSV.")
        return

    # Sidebar controls
    st.sidebar.header("Analysis Controls")
    
    # Numeric columns selection with validation
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if not numeric_cols:
        st.error("No numerical columns found in the dataset")
        return
    
    selected_cols = st.sidebar.multiselect("Select Numerical Columns", 
                                         numeric_cols, 
                                         default=numeric_cols[:2])
    
    if not selected_cols:
        st.warning("Please select at least one numerical column")
        return

    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📈 Data Overview", "📊 Visualizations", "📚 Statistics"])

    with tab1:
        st.header("Data Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dataset Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
        with col2:
            st.subheader("Column Summary")
            st.json({
                "Total Columns": len(df.columns),
                "Numerical Columns": numeric_cols,
                "Selected Columns": selected_cols
            })

    with tab2:
        st.header("Data Visualizations")
        
        # Visualization controls
        col1, col2 = st.columns(2)
        with col1:
            plot_type = st.selectbox("Select Visualization Type", [
                "Scatter Plot", 
                "Box Plot", 
                "Distribution Plot",
                "Skewness Analysis"
            ])

        with col2:
            if plot_type in ["Scatter Plot", "Distribution Plot"]:
                color_palette = st.color_picker("Select Plot Color", "#1f77b4")
            else:
                color_palette = None

        # Plot rendering
        fig = None
        if plot_type == "Scatter Plot":
            x_axis = st.selectbox("X-axis", selected_cols)
            y_axis = st.selectbox("Y-axis", [c for c in selected_cols if c != x_axis])
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(df[x_axis], df[y_axis], alpha=0.6, color=color_palette)
            ax.set_xlabel(x_axis, fontsize=12)
            ax.set_ylabel(y_axis, fontsize=12)
            ax.set_title(f"{x_axis} vs {y_axis}", fontsize=14)
            ax.grid(True, linestyle='--', alpha=0.7)

        elif plot_type == "Box Plot":
            fig, ax = plt.subplots(figsize=(10, 6))
            df[selected_cols].plot.box(ax=ax, patch_artist=True)
            ax.set_title("Distribution of Selected Columns", fontsize=14)
            ax.set_ylabel("Values", fontsize=12)
            ax.grid(True, axis='y', linestyle='--', alpha=0.7)

        elif plot_type == "Distribution Plot":
            selected = st.selectbox("Select Column", selected_cols)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.hist(df[selected], bins=20, edgecolor='white', 
                   color=color_palette, alpha=0.8)
            ax.set_title(f"Distribution of {selected}", fontsize=14)
            ax.set_xlabel(selected, fontsize=12)
            ax.set_ylabel("Frequency", fontsize=12)
            ax.grid(True, axis='y', linestyle='--', alpha=0.7)

        elif plot_type == "Skewness Analysis":
            skew_values = df[selected_cols].skew().sort_values()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            skew_values.plot.barh(ax=ax, color='#2ca02c')
            ax.set_title("Skewness of Numerical Columns", fontsize=14)
            ax.set_xlabel("Skewness Value", fontsize=12)
            ax.axvline(0, color='black', linestyle='--')
            ax.grid(True, axis='x', linestyle='--', alpha=0.7)

        if fig:
            st.pyplot(fig)
            plt.close(fig)

    with tab3:
        st.header("Statistical Summary")
        
        # Generate statistics
        stats = df[selected_cols].describe().T
        stats['skewness'] = df[selected_cols].skew()
        stats['kurtosis'] = df[selected_cols].kurtosis()
        
        # Display statistics
        st.dataframe(stats.style.format("{:.2f}").background_gradient(cmap='Blues'), 
                   use_container_width=True)
        
        # Download button
        csv = stats.to_csv().encode('utf-8')
        st.download_button(
            label="Download Statistics",
            data=csv,
            file_name='statistical_summary.csv',
            mime='text/csv'
        )

if __name__ == "__main__":
    main()