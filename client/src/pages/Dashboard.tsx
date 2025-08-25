import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Upload, MessageCircle, FileText, BarChart3, Users, Zap } from 'lucide-react';
import { documentAPI, healthAPI } from '../services/api.ts';

interface Stats {
  total_documents: number;
  total_chunks: number;
  average_chunks_per_document: number;
}

interface HealthStatus {
  status: string;
  database: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<Stats | null>(null);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsData, healthData] = await Promise.all([
          documentAPI.getStats(),
          healthAPI.checkHealth()
        ]);
        setStats(statsData);
        setHealth(healthData);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const quickActions = [
    {
      title: 'Upload Documents',
      description: 'Add new text files or paste content',
      icon: Upload,
      path: '/upload',
      color: 'bg-blue-500 hover:bg-blue-600',
    },
    {
      title: 'Start Chatting',
      description: 'Ask questions about your documents',
      icon: MessageCircle,
      path: '/chat',
      color: 'bg-green-500 hover:bg-green-600',
    },
  ];

  const statsCards = [
    {
      title: 'Total Documents',
      value: stats?.total_documents || 0,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      title: 'Text Chunks',
      value: stats?.total_chunks || 0,
      icon: BarChart3,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      title: 'Avg Chunks/Doc',
      value: stats?.average_chunks_per_document.toFixed(1) || '0',
      icon: Zap,
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Welcome to RAG Chatbot</h1>
            <p className="mt-2 text-gray-600">
              Your intelligent document assistant powered by AI
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              health?.status === 'healthy' 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {health?.status === 'healthy' ? 'System Online' : 'System Offline'}
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {quickActions.map((action) => {
          const Icon = action.icon;
          return (
            <Link
              key={action.path}
              to={action.path}
              className="group block bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200"
            >
              <div className="flex items-center">
                <div className={`p-3 rounded-lg ${action.color} text-white`}>
                  <Icon className="h-6 w-6" />
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors duration-200">
                    {action.title}
                  </h3>
                  <p className="text-gray-600">{action.description}</p>
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      {/* Statistics */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">System Statistics</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {statsCards.map((stat) => {
            const Icon = stat.icon;
            return (
              <div key={stat.title} className="flex items-center p-4 rounded-lg border border-gray-200">
                <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Features */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <Upload className="h-4 w-4 text-blue-600" />
              </div>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-900">Document Upload</h3>
              <p className="text-sm text-gray-600">Upload TXT files or paste text directly</p>
            </div>
          </div>
          
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <Zap className="h-4 w-4 text-green-600" />
              </div>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-900">Smart Embeddings</h3>
              <p className="text-sm text-gray-600">Automatic text chunking and vector generation</p>
            </div>
          </div>
          
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                <MessageCircle className="h-4 w-4 text-purple-600" />
              </div>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-900">AI Chat</h3>
              <p className="text-sm text-gray-600">Ask questions and get contextual answers</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
