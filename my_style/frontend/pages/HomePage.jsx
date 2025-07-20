import React, { useEffect, useState } from 'react';
import Card from '../components/Card';
import Button from '../components/Button';
import { fetchProducts } from '../services/apiService';
import './styles.css';

const HomePage = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getProducts = async () => {
      try {
        const data = await fetchProducts();
        setProducts(data);
      } catch (err) {
        setError('Failed to fetch products.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    getProducts();
  }, []);

  if (loading) return <div className="loading">Loading products...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="home-page">
      <h1>Welcome to Our Store!</h1>
      <div className="product-grid">
        {products.map((product) => (
          <Card
            key={product.id}
            title={product.name}
            description={product.description}
            imageUrl={product.imageUrl}
          >
            <p>Price: ${product.price.toFixed(2)}</p>
            <Button onClick={() => console.log(`Added ${product.name} to cart`)}>
              Add to Cart
            </Button>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default HomePage;