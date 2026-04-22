# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Print title
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----

# Set random seed
np.random.seed(42)

# Create 8 quarters
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022',
                  'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Store sales data here
quarterly_data = []

# Create sales data
for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales
            base_sales = np.random.normal(loc=100000, scale=20000)

            # Seasonal effect
            seasonal_factor = 1.0
            if quarter.quarter == 4:
                seasonal_factor = 1.3
            elif quarter.quarter == 1:
                seasonal_factor = 0.8

            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]

            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]

            # Growth over time
            growth_factor = (1 + 0.05 / 4) ** quarter_idx

            # Final sales amount
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)

            # Ad spend
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)

            # Save row
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Store customer data here
customer_data = []
total_customers = 2000

# Age settings by location
age_params = {
    'Tampa': (45, 15),
    'Miami': (35, 12),
    'Orlando': (38, 14),
    'Jacksonville': (42, 13)
}

# Create customer data
for location in locations:
    # Get average age and spread
    mean_age, std_age = age_params[location]

    # Customer count by location
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])

    # Create ages
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)

    # Create purchases
    for age in ages:
        # Pick category based on age
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])

        # Base purchase amount
        base_amount = np.random.gamma(shape=5, scale=20)

        # Pick price tier
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], p=[0.3, 0.5, 0.2])

        # Tier effect
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]

        # Final purchase amount
        purchase_amount = base_amount * tier_factor

        # Save row
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Make DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add extra columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print sample data
print("\nSales Data Sample:")
print(sales_df.head())

print("\nCustomer Data Sample:")
print(customer_df.head())

print("\nDataFrames created successfully. Ready for visualization!")

# ----- END OF DATA CREATION -----


# Line chart for total quarterly sales
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    # Group total sales by quarter
    df = sales_df.groupby('QuarterLabel')['Sales'].sum()

    # Make figure
    fig, ax = plt.subplots(figsize=(10, 5))

    # Create line chart
    ax.plot(df.index, df.values, marker='o', linewidth=2)

    # Add labels and title
    ax.set_title("Total Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales")
    ax.grid(True, linestyle='--', alpha=0.5)

    # Rotate quarter labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# Multi-line chart for sales by location
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    # Group sales by quarter and location
    df = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()

    # Make figure
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot one line for each location
    for location in df.columns:
        ax.plot(df.index, df[location], marker='o', linewidth=2, label=location)

    # Add labels and title
    ax.set_title("Quarterly Sales Trends by Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales")
    ax.legend(title="Location")
    ax.grid(True, linestyle='--', alpha=0.5)

    # Rotate quarter labels
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# Grouped bar chart for category sales by location
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    # Get latest quarter
    latest_quarter = sales_df['QuarterLabel'].iloc[-1]

    # Filter latest quarter
    latest_data = sales_df[sales_df['QuarterLabel'] == latest_quarter]

    # Group sales by location and category
    df = latest_data.groupby(['Location', 'Category'])['Sales'].sum().unstack()

    # Make figure
    fig, ax = plt.subplots(figsize=(11, 6))

    # Create grouped bar chart
    df.plot(kind='bar', ax=ax)

    # Add labels and title
    ax.set_title(f"Category Performance by Location ({latest_quarter})")
    ax.set_xlabel("Location")
    ax.set_ylabel("Sales")
    ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Keep x labels straight
    plt.xticks(rotation=0)
    plt.tight_layout()

    return fig


# Stacked bar chart for sales composition by location
def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    # Group sales by location and category
    df = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()

    # Convert to percentages
    df_pct = df.div(df.sum(axis=1), axis=0) * 100

    # Make figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create stacked bar chart
    df_pct.plot(kind='bar', stacked=True, ax=ax)

    # Add labels and title
    ax.set_title("Sales Composition by Location (%)")
    ax.set_xlabel("Location")
    ax.set_ylabel("Percent of Total Sales")
    ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Keep x labels straight
    plt.xticks(rotation=0)
    plt.tight_layout()

    return fig


# Scatter plot for ad spend and sales
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    # Make figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create scatter plot
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.7)

    # Create best-fit line
    z = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    p = np.poly1d(z)
    x_vals = np.linspace(sales_df['AdSpend'].min(), sales_df['AdSpend'].max(), 100)
    ax.plot(x_vals, p(x_vals), linestyle='--', linewidth=2)

    # Label top 3 sales points
    top_outliers = sales_df.nlargest(3, 'Sales')
    for _, row in top_outliers.iterrows():
        ax.annotate(
            row['Location'],
            (row['AdSpend'], row['Sales']),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=8
        )

    # Add labels and title
    ax.set_title("Advertising Spend vs Sales")
    ax.set_xlabel("Advertising Spend")
    ax.set_ylabel("Sales")
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()

    return fig


# Line chart for ad efficiency over time
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    # Group average sales per dollar by quarter
    df = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()

    # Make figure
    fig, ax = plt.subplots(figsize=(10, 5))

    # Create line chart
    ax.plot(df.index, df.values, marker='o', linewidth=2)

    # Add labels and title
    ax.set_title("Advertising Efficiency Over Time")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Average Sales per Dollar Spent")

    # Mark highest point
    max_idx = df.idxmax()
    max_val = df.max()
    ax.annotate(
        f"Peak: {max_val:.2f}",
        xy=(list(df.index).index(max_idx), max_val),
        xytext=(0, 10),
        textcoords='offset points',
        ha='center'
    )

    # Add grid
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# Histograms for customer ages
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    # Make subplots
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    axes = axes.flatten()

    # Overall ages
    overall_ages = customer_df['Age']
    axes[0].hist(overall_ages, bins=15, edgecolor='black', alpha=0.7)
    axes[0].axvline(overall_ages.mean(), linestyle='--', linewidth=2, label='Mean')
    axes[0].axvline(overall_ages.median(), linestyle=':', linewidth=2, label='Median')
    axes[0].set_title("Overall Age Distribution")
    axes[0].set_xlabel("Age")
    axes[0].set_ylabel("Frequency")
    axes[0].legend()

    # Ages by location
    for i, location in enumerate(locations, start=1):
        loc_ages = customer_df[customer_df['Location'] == location]['Age']
        axes[i].hist(loc_ages, bins=15, edgecolor='black', alpha=0.7)
        axes[i].axvline(loc_ages.mean(), linestyle='--', linewidth=2, label='Mean')
        axes[i].axvline(loc_ages.median(), linestyle=':', linewidth=2, label='Median')
        axes[i].set_title(f"{location} Age Distribution")
        axes[i].set_xlabel("Age")
        axes[i].set_ylabel("Frequency")
        axes[i].legend()

    # Hide empty box
    axes[5].axis('off')

    # Add main title
    fig.suptitle("Customer Age Distribution", fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.93)

    return fig


# Box plot for purchase amount by age group
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    # Create age groups
    bins = [18, 30, 45, 60, 100]
    labels = ['18-30', '31-45', '46-60', '61+']

    # Make copy of data
    temp_df = customer_df.copy()
    temp_df['AgeGroup'] = pd.cut(temp_df['Age'], bins=bins, labels=labels, right=True, include_lowest=True)

    # Create box plot data
    data = [temp_df[temp_df['AgeGroup'] == group]['PurchaseAmount'] for group in labels]

    # Make figure
    fig, ax = plt.subplots(figsize=(9, 5))

    # Create box plot
    ax.boxplot(data, labels=labels, patch_artist=True)

    # Add labels and title
    ax.set_title("Purchase Amount by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Purchase Amount")
    plt.tight_layout()

    return fig


# Histogram for purchase amounts
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    # Make figure
    fig, ax = plt.subplots(figsize=(9, 5))

    # Create histogram
    ax.hist(customer_df['PurchaseAmount'], bins=20, edgecolor='black', alpha=0.7)

    # Add labels and title
    ax.set_title("Distribution of Purchase Amounts")
    ax.set_xlabel("Purchase Amount")
    ax.set_ylabel("Frequency")
    ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()

    return fig


# Pie chart for sales by price tier
def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    # Group sales by price tier
    df = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()

    # Pull out biggest slice
    largest_idx = df.values.argmax()
    explode = [0, 0, 0]
    explode[largest_idx] = 0.1

    # Make figure
    fig, ax = plt.subplots(figsize=(7, 7))

    # Create pie chart
    ax.pie(df.values, labels=df.index, autopct='%1.1f%%', explode=explode, startangle=90)

    # Add title
    ax.set_title("Sales Breakdown by Price Tier")
    plt.tight_layout()

    return fig


# Pie chart for category market share
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    # Group sales by category
    df = sales_df.groupby('Category')['Sales'].sum()

    # Pull out biggest slice
    largest_idx = df.values.argmax()
    explode = [0] * len(df)
    explode[largest_idx] = 0.1

    # Make figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Create pie chart
    ax.pie(df.values, labels=df.index, autopct='%1.1f%%', explode=explode, startangle=90)

    # Add title
    ax.set_title("Market Share by Product Category")
    plt.tight_layout()

    return fig


# Pie chart for sales by location
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    # Group sales by location
    df = sales_df.groupby('Location')['Sales'].sum()

    # Make figure
    fig, ax = plt.subplots(figsize=(7, 7))

    # Create pie chart
    ax.pie(df.values, labels=df.index, autopct='%1.1f%%', startangle=90)

    # Add title
    ax.set_title("Sales Distribution by Location")
    plt.tight_layout()

    return fig


# Dashboard with main visuals
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    # Make dashboard layout
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Sales trend over time
    quarterly_sales = sales_df.groupby('QuarterLabel')['Sales'].sum()
    axes[0, 0].plot(quarterly_sales.index, quarterly_sales.values, marker='o', linewidth=2)
    axes[0, 0].set_title("Quarterly Sales Trend")
    axes[0, 0].set_xlabel("Quarter")
    axes[0, 0].set_ylabel("Sales")
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Total sales by location
    location_sales = sales_df.groupby('Location')['Sales'].sum()
    axes[0, 1].bar(location_sales.index, location_sales.values)
    axes[0, 1].set_title("Total Sales by Location")
    axes[0, 1].set_xlabel("Location")
    axes[0, 1].set_ylabel("Sales")

    # Ad spend compared to sales
    axes[1, 0].scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.7)
    axes[1, 0].set_title("Ad Spend vs Sales")
    axes[1, 0].set_xlabel("Ad Spend")
    axes[1, 0].set_ylabel("Sales")

    # Category sales share
    category_sales = sales_df.groupby('Category')['Sales'].sum()
    axes[1, 1].pie(category_sales.values, labels=category_sales.index, autopct='%1.1f%%', startangle=90)
    axes[1, 1].set_title("Category Market Share")

    # Add dashboard title
    fig.suptitle("SunCoast Retail Business Dashboard", fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)

    return fig


# Main function
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    # Run time series charts
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()

    # Run category charts
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()

    # Run ad charts
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()

    # Run customer charts
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()

    # Run purchase charts
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()

    # Run market share charts
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()

    # Run dashboard
    fig13 = create_business_dashboard()

    # Print business insights
    print("\nKEY BUSINESS INSIGHTS:")
    print("1. Overall sales trend upward over time, with strong Q4 seasonal spikes.")
    print("2. Miami appears to be the highest-performing location overall.")
    print("3. Electronics contribute the largest share of category sales.")
    print("4. Advertising spend shows a positive relationship with sales.")
    print("5. Customer age distributions differ by location, with Tampa skewing older and Miami younger.")
    print("6. Mid-range and premium pricing tiers contribute a large portion of purchase revenue.")
    print("7. The dashboard highlights major trends that can guide marketing and inventory decisions.")

    # Show all graphs
    plt.show()


# Run program
if __name__ == "__main__":
    main()