const VirtualWardrobe = ({ onClose }) => {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      fetchWardrobeItems();
    }, []);
  
    const fetchWardrobeItems = async () => {
      try {
        const response = await fetch('http://localhost:5000/wardrobe');
        const data = await response.json();
        setItems(data.items);
      } catch (error) {
        console.error('Error fetching wardrobe items:', error);
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-gray-800 rounded-lg p-6 w-full max-w-2xl">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-white">Virtual Wardrobe</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white"
            >
              ×
            </button>
          </div>
          
          {loading ? (
            <Loading />
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {items.map((item) => (
                <div
                  key={item.id}
                  className="bg-gray-700 rounded-lg p-4 hover:bg-gray-600 transition-colors"
                >
                  <h3 className="text-white font-medium">{item.name}</h3>
                  <p className="text-gray-300 text-sm">{item.type}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  };
  
  export default VirtualWardrobe;