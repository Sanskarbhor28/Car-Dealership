import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

const DealerDetails = ({ currentUser }) => {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDealerAndReviews = async () => {
      setLoading(true);
      setError('');
      try {
        // Fetch Dealer Info
        const dealerRes = await fetch(`/api/dealers/${id}/`);
        if (!dealerRes.ok) {
          throw new Error('Dealer not found');
        }
        const dealerData = await dealerRes.json();
        setDealer(dealerData);

        // Fetch Reviews
        const reviewsRes = await fetch(`/fetchReviews/dealer/${id}`);
        if (reviewsRes.ok) {
          const reviewsData = await reviewsRes.json();
          setReviews(reviewsData);
        }
      } catch (err) {
        console.error(err);
        setError('Failed to load dealer details or reviews.');
      } finally {
        setLoading(false);
      }
    };

    fetchDealerAndReviews();
  }, [id]);

  const getSentimentBadge = (sentiment) => {
    const sentLower = (sentiment || '').toLowerCase();
    if (sentLower === 'positive') {
      return <span className="badge badge-sentiment-positive px-3 py-2">Positive Sentiment 😊</span>;
    } else if (sentLower === 'negative') {
      return <span className="badge badge-sentiment-negative px-3 py-2">Negative Sentiment 😞</span>;
    } else {
      return <span className="badge badge-sentiment-neutral px-3 py-2">Neutral Sentiment 😐</span>;
    }
  };

  if (loading) {
    return (
      <div className="container text-center py-5">
        <div className="spinner-border text-primary" style={{ width: '3rem', height: '3rem' }} role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3 text-secondary">Loading dealer details & reviews...</p>
      </div>
    );
  }

  if (error || !dealer) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger text-center shadow-sm" role="alert">
          {error || 'Dealer not found.'}
        </div>
        <div className="text-center">
          <Link to="/" className="btn btn-secondary">Back to Dealers</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mb-5">
      {/* Dealer Header Info Card */}
      <div className="card shadow border-0 mb-4 bg-primary text-white rounded-3">
        <div className="card-body p-4 d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3">
          <div>
            <h2 className="fw-bold mb-1">{dealer.full_name}</h2>
            <p className="mb-2 text-white-50">
              Dealer ID: <span className="fw-bold text-light">{dealer.dealer_id || dealer.id}</span>
            </p>
            <div className="d-flex flex-wrap gap-3">
              <span>📍 <strong>Address:</strong> {dealer.address}, {dealer.city}, {dealer.state} {dealer.zip}</span>
              <span>📞 <strong>Phone:</strong> {dealer.phone}</span>
            </div>
          </div>

          <div>
            {currentUser ? (
              <Link to={`/postreview/${dealer.dealer_id || dealer.id}`} className="btn btn-light btn-lg fw-bold text-primary shadow-sm">
                ✏️ Post a Review
              </Link>
            ) : (
              <Link to="/login" className="btn btn-warning btn-lg fw-bold shadow-sm">
                Log in to Post Review
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Reviews Header */}
      <div className="d-flex align-items-center justify-content-between mb-4">
        <h3 className="fw-bold text-dark mb-0">Customer Reviews ({reviews.length})</h3>
        <Link to="/" className="btn btn-outline-secondary btn-sm">
          ← Back to All Dealers
        </Link>
      </div>

      {/* Reviews Grid */}
      {reviews.length === 0 ? (
        <div className="card shadow-sm border-0 text-center py-5">
          <div className="card-body">
            <h5 className="text-muted mb-3">No reviews yet for {dealer.full_name}.</h5>
            {currentUser && (
              <Link to={`/postreview/${dealer.dealer_id || dealer.id}`} className="btn btn-primary">
                Be the first to review this dealer!
              </Link>
            )}
          </div>
        </div>
      ) : (
        <div className="row g-4">
          {reviews.map((rev) => (
            <div key={rev.id} className="col-md-6">
              <div className="card shadow-sm h-100 border-0 rounded-3">
                <div className="card-header bg-light d-flex align-items-center justify-content-between border-0 py-3">
                  <div>
                    <h5 className="fw-bold text-dark mb-0">{rev.name || 'Anonymous Reviewer'}</h5>
                    <div className="text-warning">
                      {'★'.repeat(rev.rating || 5)}{'☆'.repeat(5 - (rev.rating || 5))}
                    </div>
                  </div>
                  <div>{getSentimentBadge(rev.sentiment)}</div>
                </div>

                <div className="card-body">
                  <p className="card-text text-dark fs-6 lead">"{rev.review}"</p>

                  {rev.purchase && (
                    <div className="bg-light p-2 rounded text-secondary small">
                      🚗 <strong>Purchased:</strong> {rev.car_make} {rev.car_model} ({rev.car_year})
                      {rev.purchase_date && <span> on {rev.purchase_date}</span>}
                    </div>
                  )}
                </div>

                <div className="card-footer bg-white border-0 text-muted small">
                  Posted on: {rev.created_at ? new Date(rev.created_at).toLocaleDateString() : 'Recent'}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DealerDetails;
