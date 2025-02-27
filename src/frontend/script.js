document.addEventListener("DOMContentLoaded", function() {
    const API_URL = "https://gerador-estrutura-projetos-nrk2.onrender.com/gerar-estrutura"; // 🔹 URL do backend no Render

    // Botão para gerar estrutura
    document.getElementById("generateBtn").addEventListener("click", async function(event) {
        event.preventDefault(); // 🔹 Evita comportamento padrão de formulário

        const inputText = document.getElementById("inputText").value;

        if (!inputText.trim()) {
            alert("⚠️ Por favor, digite uma estrutura antes de gerar o código!");
            return;
        }

        alert("➡️ Enviando requisição para API...\n🔹 URL: " + API_URL + "\n🔹 Método: POST");

        try {
            const response = await fetch(API_URL, {  
                method: "POST",  
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estrutura: inputText })
            });

            alert("⬅️ Resposta recebida da API...\n🔹 Status: " + response.status);

            const data = await response.json();
            alert("🔹 Resposta JSON:\n" + JSON.stringify(data, null, 2));

            if (response.ok) {
                document.getElementById("outputCode").textContent = data.codigo.replace(/\n/g, "\n");
                alert("✅ Código gerado com sucesso!");
            } else {
                alert("❌ Erro ao gerar código:\n" + (data.erro || "Erro desconhecido."));
            }
        } catch (error) {
            alert("🚨 Erro ao conectar com o servidor:\n" + error);
        }
    });

    // Botão para copiar código
    document.getElementById("copyBtn").addEventListener("click", function() {
        const outputCode = document.getElementById("outputCode").textContent;
        
        if (!outputCode.trim()) {
            alert("⚠️ Nenhum código gerado para copiar!");
            return;
        }

        navigator.clipboard.writeText(outputCode)
            .then(() => alert("✅ Código copiado para a área de transferência!"))
            .catch(err => alert("❌ Erro ao copiar código: " + err));
    });

    // Botão para baixar código como .py
    document.getElementById("downloadBtn").addEventListener("click", function() {
        const outputCode = document.getElementById("outputCode").textContent;
        
        if (!outputCode.trim()) {
            alert("⚠️ Nenhum código gerado para baixar!");
            return;
        }

        const blob = new Blob([outputCode], { type: "text/plain" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "gerar_estrutura.py";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        alert("📥 Download iniciado!");
    });
});
