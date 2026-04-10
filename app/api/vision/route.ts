import { NextResponse } from 'next/server';

const API_KEY = "sk-w7Eit87AWrFGwLYLrIcSOgdDW204j0euC2Zlg5DACz4xx7nT";
const API_ENDPOINT = "https://happyapi.org/v1/chat/completions";
const VISION_MODEL = "grok-3";

export async function POST(req: Request) {
  try {
    const { image, prompt } = await req.json();

    if (!image) {
      return NextResponse.json({ error: "Image is required" }, { status: 400 });
    }

    const apiKey = "sk-w7Eit87AWrFGwLYLrIcSOgdDW204j0euC2Zlg5DACz4xx7nT";
    const apiEndpoint = "https://happyapi.org/v1/chat/completions";
    const model = "grok-3";

    const systemPrompt = `You are an expert AI art prompter. Your task is to analyze the provided image and generate a high-quality, detailed text prompt based on the user's instruction.
    
    User Instruction: ${prompt}
    
    Output Format:
    Strictly output ONLY the prompt text. Do not include "Here is the prompt" or any other conversational text.
    The prompt should be in English, comma-separated tags or sentences, suitable for AI image generation.`;

    const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`
        },
        body: JSON.stringify({
          model: model,
          messages: [
          {
            role: "system",
            content: systemPrompt
          },
          {
            role: "user",
            content: [
              { type: "text", text: "Analyze this image and generate the prompt." },
              {
                type: "image_url",
                image_url: {
                  url: image // Assumes base64 data:image/jpeg;base64,...
                }
              }
            ]
          }
        ],
        max_tokens: 500
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Vision API Error:", errorText);
      return NextResponse.json({ error: `Vision API Error: ${response.status} - ${errorText}` }, { status: response.status });
    }

    const data = await response.json();
    const content = data.choices[0].message.content;

    return NextResponse.json({ prompt: content });

  } catch (error: any) {
    console.error("Vision Route Error:", error);
    return NextResponse.json(
      { error: error.message || "Internal Server Error" },
      { status: 500 }
    );
  }
}
