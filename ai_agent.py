import google.generativeai as genai
from google.ai.generativelanguage import DiscussServiceClient, MessagePrompt, GenerateMessageRequest, GenerationConfig
from google.api_core import client_options
from dotenv import load_dotenv
from google.api_core.exceptions import NotFound
from data import obter_dados_fiis
import os


load_dotenv()

class GeminiAgent:
    def __init__(self, model_name="gemini-1.5-flash-002"): # Set Default Value Here.
        self.api_key = os.getenv("gemini_api")
        if not self.api_key:
            raise ValueError("Erro: Chave da API não encontrada.  Verifique se a variável de ambiente 'gemini_api' está definida corretamente.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.chat = self.model.start_chat(history=[])


    def get_response(self, prompt):
        """
        Gets a response from the Gemini model.
        """
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Erro ao obter resposta da API: {e}"

def analyze_fii_with_ai(fii_code):
    """Analisa um FII usando IA com dados fundamentais"""
    agent = GeminiAgent()
    if not agent.api_key:
        return "Erro: Chave da API não configurada."
    
    try:
        # Buscar dados diretamente da fonte principal
        df_fiis = obter_dados_fiis()
        df_fii_data = df_fiis[df_fiis['código'] == fii_code]
        
        if df_fii_data.empty:
            return "FII não encontrado na base de dados."
            
        # Construir contexto apenas com dados fundamentais
        context = f"""
        Você é um especialista em Fundos Imobiliários (FIIs) no Brasil. 
        Analise o FII {fii_code} com base nestes dados fundamentais:

        {df_fii_data.iloc[0].to_string()}
        """
        
        prompt = f"""
        {context}
        
        Forneça:
        1. Faça uma análise fundamentalista de indicadores chaves deste FII
        2. Identifique pontos fortes e fracos
        3. Recomendação baseada nos fundamentos
        4. Perspectivas de curto/médio prazo
        
        Formato: Lista concisa em português (máx. 350 caracteres)
        """
        
        return agent.get_response(prompt)
    
    except Exception as e:
        return f"Erro na análise: {str(e)}"
