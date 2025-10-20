/**
 * Home/Landing Page
 * 
 * Public landing page showcasing DataLens features
 */

import { Link } from 'react-router-dom';
import { Database, BarChart3, Sparkles, Upload, TrendingUp, Brain, Shield, Zap, Users } from 'lucide-react';

const Home = () => {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2">
              <span className="text-2xl font-bold text-primary-500">DataLens</span>
            </Link>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-gray-600 hover:text-navy-900 transition-colors">
                Features
              </a>
              <a href="#tech-stack" className="text-gray-600 hover:text-navy-900 transition-colors">
                Tech Stack
              </a>
              <a href="https://github.com/22CB006" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-navy-900 transition-colors">
                GitHub
              </a>
            </div>

            {/* Auth Buttons */}
            <div className="flex items-center gap-4">
              <Link
                to="/login"
                className="text-navy-900 hover:text-navy-700 font-medium transition-colors"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="bg-primary-500 hover:bg-primary-600 text-white font-semibold px-6 py-2 rounded-lg transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="text-navy-900">Transform Your Data Into</span>
            <br />
            <span className="bg-gradient-to-r from-primary-500 via-pink-500 to-blue-500 bg-clip-text text-transparent">
              Actionable Insights
            </span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto">
            Upload, analyze, and visualize your datasets with powerful AI-driven insights. 
            Built with modern technologies for seamless data exploration.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/register"
              className="bg-primary-500 hover:bg-primary-600 text-white font-semibold px-8 py-4 rounded-lg transition-colors flex items-center gap-2 text-lg"
            >
              Get Started →
            </Link>
            <button className="border-2 border-gray-300 hover:border-navy-900 text-navy-900 font-semibold px-8 py-4 rounded-lg transition-colors text-lg">
              View Demo
            </button>
          </div>
        </div>
      </section>

      {/* Features Grid - Top 3 */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            {/* Smart Upload */}
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-2xl mb-4">
                <Database className="w-8 h-8 text-primary-500" />
              </div>
              <h3 className="text-xl font-bold text-navy-900 mb-2">Smart Upload</h3>
              <p className="text-gray-600">
                CSV, Excel, JSON support with automatic validation
              </p>
            </div>

            {/* Advanced Analytics */}
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-2xl mb-4">
                <BarChart3 className="w-8 h-8 text-blue-500" />
              </div>
              <h3 className="text-xl font-bold text-navy-900 mb-2">Advanced Analytics</h3>
              <p className="text-gray-600">
                Statistical analysis with correlation & trend detection
              </p>
            </div>

            {/* AI Insights */}
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-2xl mb-4">
                <Sparkles className="w-8 h-8 text-primary-500" />
              </div>
              <h3 className="text-xl font-bold text-navy-900 mb-2">AI Insights</h3>
              <p className="text-gray-600">
                Automated insights and predictive analytics
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack Badges */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div className="bg-white border border-gray-200 rounded-xl p-6">
              <div className="text-4xl font-bold text-primary-500 mb-2">100%</div>
              <div className="text-navy-900 font-semibold mb-1">Type Safe</div>
              <div className="text-sm text-gray-600">Full TypeScript & Python typing</div>
            </div>

            <div className="bg-white border border-gray-200 rounded-xl p-6">
              <div className="text-4xl font-bold text-blue-500 mb-2">FastAPI</div>
              <div className="text-navy-900 font-semibold mb-1">Async Backend</div>
              <div className="text-sm text-gray-600">Modern async Python framework</div>
            </div>

            <div className="bg-white border border-gray-200 rounded-xl p-6">
              <div className="text-4xl font-bold text-primary-500 mb-2">JWT</div>
              <div className="text-navy-900 font-semibold mb-1">Secure Auth</div>
              <div className="text-sm text-gray-600">Industry-standard authentication</div>
            </div>

            <div className="bg-white border border-gray-200 rounded-xl p-6">
              <div className="text-4xl font-bold text-blue-500 mb-2">CI/CD</div>
              <div className="text-navy-900 font-semibold mb-1">Automated</div>
              <div className="text-sm text-gray-600">GitHub Actions pipeline</div>
            </div>
          </div>
        </div>
      </section>

      {/* Powerful Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              <span className="text-navy-900">Powerful Features for</span>
              <br />
              <span className="bg-gradient-to-r from-primary-500 to-pink-400 bg-clip-text text-transparent">
                Data Excellence
              </span>
            </h2>
            <p className="text-xl text-gray-600">
              Everything you need to transform raw data into meaningful insights
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Multi-Format Upload */}
            <div className="bg-white rounded-xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="inline-flex items-center justify-center w-14 h-14 bg-primary-100 rounded-2xl mb-4">
                <Upload className="w-7 h-7 text-primary-500" />
              </div>
              <h3 className="text-xl font-bold text-navy-900 mb-3">Multi-Format Upload</h3>
              <p className="text-gray-600">
                Seamlessly upload CSV, Excel, or JSON files. Automatic validation ensures data integrity from the start.
              </p>
            </div>

            {/* Interactive Visualizations */}
            <div className="bg-white rounded-xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="inline-flex items-center justify-center w-14 h-14 bg-blue-100 rounded-2xl mb-4">
                <TrendingUp className="w-7 h-7 text-blue-500" />
              </div>
              <h3 className="text-xl font-bold text-navy-900 mb-3">Interactive Visualizations</h3>
              <p className="text-gray-600">
                Dynamic charts and graphs powered by Chart.js and Plotly. Explore your data with beautiful, responsive visualizations.
              </p>
            </div>

            {/* AI-Powered Analysis */}
            <div className="bg-white rounded-xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="inline-flex items-center justify-center w-14 h-14 bg-primary-100 rounded-2xl mb-4">
                <Brain className="w-7 h-7 text-primary-500" />
              </div>
              <h3 className="text-xl font-bold text-navy-900 mb-3">AI-Powered Analysis</h3>
              <p className="text-gray-600">
                Leverage machine learning for predictive analytics, anomaly detection, and automated insight generation.
              </p>
            </div>

            {/* Secure Authentication */}
            <div className="bg-white rounded-xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="inline-flex items-center justify-center w-14 h-14 bg-blue-100 rounded-2xl mb-4">
                <Shield className="w-7 h-7 text-blue-500" />
              </div>
              <h3 className="text-xl font-bold text-navy-900 mb-3">Secure Authentication</h3>
              <p className="text-gray-600">
                Enterprise-grade security with JWT authentication, role-based access control, and encrypted data storage.
              </p>
            </div>

            {/* Real-Time Processing */}
            <div className="bg-white rounded-xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="inline-flex items-center justify-center w-14 h-14 bg-primary-100 rounded-2xl mb-4">
                <Zap className="w-7 h-7 text-primary-500" />
              </div>
              <h3 className="text-xl font-bold text-navy-900 mb-3">Real-Time Processing</h3>
              <p className="text-gray-600">
                Fast, asynchronous data processing with Pandas and NumPy. Handle large datasets with ease and speed.
              </p>
            </div>

            {/* Collaboration Ready */}
            <div className="bg-white rounded-xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="inline-flex items-center justify-center w-14 h-14 bg-blue-100 rounded-2xl mb-4">
                <Users className="w-7 h-7 text-blue-500" />
              </div>
              <h3 className="text-xl font-bold text-navy-900 mb-3">Collaboration Ready</h3>
              <p className="text-gray-600">
                Share insights, export reports, and collaborate with your team. Built for modern data-driven workflows.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section id="tech-stack" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              <span className="text-navy-900">Built With</span>
              <br />
              <span className="bg-gradient-to-r from-primary-500 to-pink-400 bg-clip-text text-transparent">
                Modern Technologies
              </span>
            </h2>
            <p className="text-xl text-gray-600">
              Leveraging industry-standard tools and frameworks for production-ready applications
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            {/* Backend */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-3 h-3 bg-primary-500 rounded-full"></div>
                <h3 className="text-2xl font-bold text-navy-900">Backend</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                <span className="px-4 py-2 bg-teal-100 text-teal-700 rounded-full text-sm font-medium">FastAPI</span>
                <span className="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">Python 3.11+</span>
                <span className="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">Pandas & NumPy</span>
                <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">PostgreSQL</span>
                <span className="px-4 py-2 bg-red-100 text-red-700 rounded-full text-sm font-medium">SQLAlchemy</span>
                <span className="px-4 py-2 bg-orange-100 text-orange-700 rounded-full text-sm font-medium">JWT Auth</span>
              </div>
            </div>

            {/* Frontend */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <h3 className="text-2xl font-bold text-navy-900">Frontend</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                <span className="px-4 py-2 bg-cyan-100 text-cyan-700 rounded-full text-sm font-medium">React 18</span>
                <span className="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">Vite</span>
                <span className="px-4 py-2 bg-cyan-100 text-cyan-700 rounded-full text-sm font-medium">TailwindCSS</span>
                <span className="px-4 py-2 bg-gray-100 text-gray-700 rounded-full text-sm font-medium">shadcn/ui</span>
                <span className="px-4 py-2 bg-pink-100 text-pink-700 rounded-full text-sm font-medium">Chart.js</span>
                <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">Axios</span>
              </div>
            </div>

            {/* DevOps */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-3 h-3 bg-primary-500 rounded-full"></div>
                <h3 className="text-2xl font-bold text-navy-900">DevOps</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">Docker</span>
                <span className="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium">GitHub Actions</span>
                <span className="px-4 py-2 bg-gray-100 text-gray-700 rounded-full text-sm font-medium">Vercel</span>
                <span className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">PostgreSQL Cloud</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            {/* Brand */}
            <div>
              <h3 className="text-2xl font-bold text-primary-500 mb-4">DataLens</h3>
              <p className="text-gray-600">
                Built with modern technologies to showcase full-stack development, data engineering, and cloud deployment skills.
              </p>
            </div>

            {/* Project Links */}
            <div>
              <h4 className="font-semibold text-navy-900 mb-4">Project Links</h4>
              <ul className="space-y-2">
                <li>
                  <a href="#features" className="text-gray-600 hover:text-navy-900 transition-colors">Features</a>
                </li>
                <li>
                  <a href="#tech-stack" className="text-gray-600 hover:text-navy-900 transition-colors">Tech Stack</a>
                </li>
                <li>
                  <a href="https://github.com/22CB006/DataLens---Intelligent-Data-Dashboard-Web-App" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-navy-900 transition-colors">
                    Documentation
                  </a>
                </li>
              </ul>
            </div>

            {/* Connect */}
            <div>
              <h4 className="font-semibold text-navy-900 mb-4">Connect</h4>
              <div className="flex gap-4 mb-4">
                <a href="https://github.com/22CB006" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-navy-900 transition-colors">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                </a>
                <a href="https://www.linkedin.com/in/aryalakshmi/" target="_blank" rel="noopener noreferrer" className="text-gray-600 hover:text-navy-900 transition-colors">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                  </svg>
                </a>
              </div>
              <p className="text-sm text-gray-600">
                <strong>Arya Lakshmi M</strong><br />
                Full-Stack Developer
              </p>
            </div>
          </div>

          <div className="mt-8 pt-8 border-t border-gray-200 text-center text-sm text-gray-600">
            © 2025 DataLens. Built as a portfolio project to demonstrate modern web development skills.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
