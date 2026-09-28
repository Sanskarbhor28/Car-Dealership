import React, { useState, useEffect } from 'react';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';

const Dealers = ({ currentUser }) => {
  const [dealers, setDealers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedState, setSelectedState] = useState('All');
  
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const states = ['All', 'Kansas', 'Texas', 'California', 'New York'];

  const fetchDealers = async (stateFilter) => {
    setLoading(true);
    setError('');
    try {
      let url = '/fetchDealers';
      if (stateFilter && stateFilter !== 'All') {
        url += `?state=${encodeURIComponent(stateFilter)}`;
      }
      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`Error fetching dealers: ${res.statusText}`);
      }
      const data = await res.json();
      setDealers(data);
    } catch (err) {
      console.error(err);
      setError('Failed to load dealer listings. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const stateFromUrl = searchParams.get('state') || 'All';
    setSelectedState(stateFromUrl);
    fetchDealers(stateFromUrl);
  }, [searchParams]);

  const handleStateChange = (e) => {
    const newState = e.target.value;
    setSelectedState(newState);
    if (newState === 'All') {
      setSearchParams({});
    } else {
      setSearchParams({ state: newState });
    }
  };

  return (
    <div className="container">
      {/* Hero Header Banner */}
      <div className="hero-banner shadow text-center">
        <h1 className="display-4 fw-bold">National Dealership Network</h1>
        <p className="lead text-white-50">
          Find top-rated certified dealerships, browse vehicle models, and read verified reviews across the United States.
        </p>
      </div>

      {/* Filter and Search Controls */}
      <div className="card shadow-sm mb-4 border-0">
        <div className="card-body d-flex flex-column flex-md-row align-items-center justify-content-between gap-3">
          <div className="d-flex align-items-center gap-2 w-100 w-md-auto">
            <label htmlFor="state-select" className="fw-bold text-dark me-2 mb-0 text-nowrap">
              Filter by State:
            </label>
            <select
              id="state-select"
              className="form-select form-select-lg border-primary"
              value={selectedState}
              onChange={handleStateChange}
              style={{ minWidth: '220px' }}
            >
              {states.map((st) => (
                <option key={st} value={st}>
                  {st === 'All' ? 'All States (Show All)' : st}
                </option>
              ))}
            </select>
          </div>

          <div className="text-secondary fw-semibold">
            Showing <span className="text-primary fw-bold fs-5">{dealers.length}</span> Dealerships
            {selectedState !== 'All' && <span> in <span className="badge bg-primary fs-6">{selectedState}</span></span>}
          </div>
        </div>
      </div>

      {/* Loading state */}
      {loading && (
        <div className="text-center py-5">
          <div className="spinner-border text-primary" style={{ width: '3rem', height: '3rem' }} role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3 text-secondary">Loading dealerships...</p>
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="alert alert-danger text-center shadow-sm" role="alert">
          {error}
        </div>
      )}

      {/* Dealers List / Table */}
      {!loading && !error && dealers.length === 0 && (
        <div className="alert alert-warning text-center shadow-sm py-4">
          <h4 className="fw-bold">No Dealerships Found</h4>
          <p className="mb-0">There are currently no dealers listed for {selectedState}.</p>
        </div>
      )}

      {!loading && !error && dealers.length > 0 && (
        <div className="card shadow-sm border-0 mb-5">
          <div className="table-responsive">
            <table className="table table-hover table-striped align-middle mb-0">
              <thead className="table-dark">
                <tr>
                  <th scope="col">ID</th>
                  <th scope="col">Dealer Name</th>
                  <th scope="col">City</th>
                  <th scope="col">State</th>
                  <th scope="col">Address</th>
                  <th scope="col">Zip</th>
                  <th scope="col">Phone</th>
                  <th scope="col" className="text-center">Action</th>
                </tr>
              </thead>
              <tbody>
                {dealers.map((dealer) => (
                  <tr key={dealer.id || dealer.dealer_id}>
                    <td className="fw-bold">{dealer.dealer_id || dealer.id}</td>
                    <td>
                      <Link to={`/dealer/${dealer.dealer_id || dealer.id}`} className="fw-bold text-primary text-decoration-none fs-6">
                        {dealer.full_name}
                      </Link>
                    </td>
                    <td>{dealer.city}</td>
                    <td>
                      <span className="badge bg-secondary">{dealer.state}</span>
                    </td>
                    <td>{dealer.address}</td>
                    <td>{dealer.zip}</td>
                    <td>{dealer.phone}</td>
                    <td className="text-center">
                      <div className="d-flex justify-content-center gap-2">
                        <Link
                          to={`/dealer/${dealer.dealer_id || dealer.id}`}
                          className="btn btn-sm btn-outline-primary fw-semibold"
                        >
                          View Reviews
                        </Link>
                        {currentUser && (
                          <Link
                            to={`/postreview/${dealer.dealer_id || dealer.id}`}
                            className="btn btn-sm btn-success fw-semibold"
                            id={`review-dealer-btn-${dealer.dealer_id || dealer.id}`}
                          >
                            ✏️ Review Dealer
                          </Link>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dealers;
