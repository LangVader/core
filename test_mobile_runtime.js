// Test directo del Vader Runtime Móvil
const fs = require('fs');

// Cargar el runtime
eval(fs.readFileSync('./vader-7.0-universal-mobile.js', 'utf8'));

// Cargar código de prueba
const vaderCode = fs.readFileSync('./test_mobile_nativo.vdr', 'utf8');

// Crear instancia y ejecutar
const mobile = new VaderUniversalMobile();

mobile.execute(vaderCode).then(result => {
    if (result.error) {
        console.log('❌ Error:', result.error);
    } else {
        console.log('✅ Archivo .vdr móvil ejecutado nativamente');
        console.log('📱 Plataforma:', result.platform);
        console.log('🎯 Contexto:', result.context);
        console.log('🌍 Idioma:', result.language);
        console.log('📄 Código React Native generado:');
        console.log('='.repeat(50));
        console.log(result.output);
        console.log('='.repeat(50));
    }
}).catch(err => {
    console.log('❌ Error:', err.message);
});
