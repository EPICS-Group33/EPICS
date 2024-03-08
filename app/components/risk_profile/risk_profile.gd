extends Resource
class_name RiskProfile

# Blood Report

# Complete Blood Count (CBC)
var rbc_count : int
var wbc_count : int
var platelet_count : int
var hematocrit_levels : float # Percentage of rbc in blood
var hemoglobin_level : float
var rdw_value : float # RDW-RBC Distribution Width, Variations in rbc size and volume
var mcv_value : float # MCW-Mean Corpuscular Volume, Average size of RBC

# Basic metabolic Panel (BMP)
var glucose_level : float
var calcium_level : float
var bun_level : float # BUN-Blood Urea Nitrogen, Amount of urea in blood
var ck_level : float # Ck-Creatine Kinase, Waste product from muscles, indicates muscle wear
var na_levels : float # Na-Sodium
var co2_level : float
var serumk_level : float # Serum Pottasium Level
var cl_level : float
var globulin_level : float

# Comprehensive Metabolic Panel (CMP)
var albumin_level : float
var alt_level : float # ALT-Alanine Transamine
var alkaline_level : float
var ammonia
