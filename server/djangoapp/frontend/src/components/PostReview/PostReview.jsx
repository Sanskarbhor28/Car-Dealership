import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';

const PostReview = ({ currentUser }) => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [dealer, setDealer] = useState(null);
  const [carMakes, setCarMakes] = useState([]);
  const [selectedMake, setSelectedMake] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [availableModels, setAvailableModels] = useState([]);

  const [reviewText, setReviewText] = useState('');
  const [rating, setRating] = useState(5);
  const [purchase, setPurchase] = useState(false);
  const [purchaseDate, setPurchaseDate] = useState('');
  const [carYear, setCarYear] = useState(2023);

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!currentUser) {
      navigate('/login');
      return;
    }

    const fetchData = async () => {
      setLoading(true);
      try {
        // 1. Fetch Dealer Info
        const dealerRes = await fetch(`/api/dealers/${id}/`);
        if (dealerRes.ok) {
          const dealerData = await dealerRes.json();
          setDealer(dealerData);
        }

        // 2. Fetch Car Makes and Models
        const carsRes = await fetch('/api/carmakes/');
        if (carsRes.ok) {
          const carsData = await carsRes.json();
          setCarMakes(carsData.CarMakes || []);
        }
      } catch (err) {
        console.error(err);
        setError('Error loading initial review data.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id, currentUser, navigate]);

  const handleMakeChange = (e) => {
    const makeName = e.target.value;
    setSelectedMake(makeName);
    setSelectedModel('');

    const foundMake = carMakes.find((m) => m.name === makeName);
    if (foundMake && foundMake.models) {
      setAvailableModels(foundMake.models);
    } else {
      setAvailableModels([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!reviewText.trim()) {
      setError('Please write your review before submitting.');
      return;
    }

    setSubmitting(true);

    const payload = {
      dealer_id: parseInt(id, 10),
      name: currentUser || 'Anonymous',
      review: reviewText,
      rating: parseInt(rating, 10),
      purchase: purchase,
      purchase_date: purchase ? purchaseDate : null,
      car_make: selectedMake,
      car_model: selectedModel,
      car_year: purchase ? parseInt(carYear, 10) : null,
    };

    try {
      const res = await fetch('/api/reviews/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        navigate(`/dealer/${id}`);
      } else {
        const errData = await res.json();
        setError(errData.error || 'Failed to post review.');
      }
    } catch (err) {
      console.error(err);
      setError('Network error submitting review.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="container text-center py-5">
        <div className="spinner-border text-primary" style={{ width: '3rem', height: '3rem' }} role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4 mb-5">
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-7">
          <div className="card shadow-lg border-0 rounded-3">
            <div className="card-header bg-primary text-white py-3">
              <h3 className="card-title fw-bold mb-0">Write a Review for {dealer?.full_name || 'Dealer'}</h3>
              <p className="mb-0 text-white-50">
                Dealer ID: {id} | Logged in as: <strong>{currentUser}</strong>
              </p>
            </div>

            <div className="card-body p-4">
              {error && (
                <div className="alert alert-danger alert-dismissible fade show" role="alert">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                {/* Review Text */}
                <div className="mb-3">
                  <label htmlFor="review-text" className="form-label fw-bold">
                    Your Review / Comments *
                  </label>
                  <textarea
                    id="review-text"
                    className="form-control"
                    rows="4"
                    placeholder="Describe your overall experience, customer service, vehicle condition, pricing..."
                    value={reviewText}
                    onChange={(e) => setReviewText(e.target.value)}
                    required
                  ></textarea>
                </div>

                {/* Rating */}
                <div className="mb-3">
                  <label htmlFor="rating-select" className="form-label fw-bold">
                    Rating (1 to 5 Stars)
                  </label>
                  <select
                    id="rating-select"
                    className="form-select"
                    value={rating}
                    onChange={(e) => setRating(e.target.value)}
                  >
                    <option value="5">5 Stars - Excellent</option>
                    <option value="4">4 Stars - Very Good</option>
                    <option value="3">3 Stars - Average</option>
                    <option value="2">2 Stars - Poor</option>
                    <option value="1">1 Star - Terrible</option>
                  </select>
                </div>

                {/* Purchase Checkbox */}
                <div className="form-check mb-3">
                  <input
                    type="checkbox"
                    className="form-check-input"
                    id="purchase-check"
                    checked={purchase}
                    onChange={(e) => setPurchase(e.target.checked)}
                  />
                  <label className="form-check-label fw-semibold" htmlFor="purchase-check">
                    Has purchased a vehicle from this dealership?
                  </label>
                </div>

                {/* Conditional Purchase Fields */}
                {purchase && (
                  <div className="bg-light p-3 rounded-3 mb-3 border">
                    <h6 className="fw-bold mb-3 text-secondary">Vehicle & Purchase Information</h6>
                    <div className="row g-3">
                      <div className="col-md-6">
                        <label htmlFor="car-make-select" className="form-label fw-bold">
                          Car Make
                        </label>
                        <select
                          id="car-make-select"
                          className="form-select"
                          value={selectedMake}
                          onChange={handleMakeChange}
                        >
                          <option value="">-- Select Car Make --</option>
                          {carMakes.map((m) => (
                            <option key={m.id} value={m.name}>
                              {m.name}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="col-md-6">
                        <label htmlFor="car-model-select" className="form-label fw-bold">
                          Car Model
                        </label>
                        <select
                          id="car-model-select"
                          className="form-select"
                          value={selectedModel}
                          onChange={(e) => setSelectedModel(e.target.value)}
                          disabled={!selectedMake}
                        >
                          <option value="">-- Select Car Model --</option>
                          {availableModels.map((mod) => (
                            <option key={mod.id} value={mod.name}>
                              {mod.name} ({mod.type})
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="col-md-6">
                        <label htmlFor="purchase-date" className="form-label fw-bold">
                          Purchase Date
                        </label>
                        <input
                          type="date"
                          id="purchase-date"
                          className="form-control"
                          value={purchaseDate}
                          onChange={(e) => setPurchaseDate(e.target.value)}
                        />
                      </div>

                      <div className="col-md-6">
                        <label htmlFor="car-year" className="form-label fw-bold">
                          Vehicle Year
                        </label>
                        <input
                          type="number"
                          id="car-year"
                          className="form-control"
                          min="2010"
                          max="2030"
                          value={carYear}
                          onChange={(e) => setCarYear(e.target.value)}
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* Buttons */}
                <div className="d-flex justify-content-between align-items-center mt-4">
                  <Link to={`/dealer/${id}`} className="btn btn-outline-secondary">
                    Cancel
                  </Link>
                  <button
                    type="submit"
                    className="btn btn-success btn-lg fw-bold px-4"
                    disabled={submitting}
                    id="submit-review-btn"
                  >
                    {submitting ? 'Submitting...' : 'Submit Review'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
