const barcodeResult = document.getElementById('barcode-result');
const video = document.getElementById('barcode-scanner');

// Verifica si el navegador es compatible con la API de MediaDevices
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    .then(function(stream) {
        // Configura la corriente de video en el elemento de video
        video.srcObject = stream;
        video.play();

        // Utiliza la API de Barcode Detection para detectar códigos de barras
        const barcodeDetector = new BarcodeDetector();

        video.addEventListener('loadedmetadata', () => {
            // Ajusta el tamaño del canvas según las dimensiones del video
            const canvas = document.createElement('canvas');
            const canvasContext = canvas.getContext('2d');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            // Cada cierto intervalo, detecta códigos de barras en el video
            setInterval(async () => {
                canvasContext.drawImage(video, 0, 0, canvas.width, canvas.height);
                const barcodes = await barcodeDetector.detect(canvas);
                
                // Muestra el código de barras detectado (si hay alguno) en la página
                if (barcodes.length > 0) {
                    barcodeResult.innerHTML = `Código de barras detectado: ${barcodes[0].rawValue}`;
                } else {
                    barcodeResult.innerHTML = 'Escaneando...';
                }
            }, 1000); // Intervalo de detección (cada segundo en este ejemplo)
        });
    })
    .catch(function(error) {
        console.error('Error al acceder a la cámara:', error);
    });
} else {
    console.error('La API de MediaDevices no está soportada en este navegador.');
}
