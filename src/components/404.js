import React, {useEffect} from 'react';
import './Styles/404.css';

function NotFound() {
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [])
    document.title = "404 - Page not found";
  return (
    <div className="page-not-found"
    >
      <h1 data-content="404">404</h1>
      <p>Page not foundt</p>
    </div>
  );
}

export default NotFound;